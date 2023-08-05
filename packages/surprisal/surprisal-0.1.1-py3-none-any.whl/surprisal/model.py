import typing
import logging
from abc import abstractmethod
from functools import partial

import numpy as np
from transformers import (
    AutoModelForCausalLM,
    AutoModelForMaskedLM,
    AutoTokenizer,
    PreTrainedModel,
)

from surprisal.utils import pick_matching_token_ixs
from surprisal.interface import Model, SurprisalArray, SurprisalQuantity

logger = logging.getLogger(name="surprisal")


class HuggingFaceSurprisal(SurprisalArray):
    def __init__(
        self,
        tokens: "Encoding",
        surprisals: np.ndarray,
    ) -> None:
        super().__init__()

        self._tokens: "Encoding" = tokens
        self._surprisals = surprisals.astype(SurprisalQuantity)

    @property
    def tokens(self):
        return self._tokens.tokens

    @property
    def surprisals(self):
        return self._surprisals

    def __iter__(self) -> typing.Tuple[str, float]:
        return zip(self.tokens, self.surprisals)

    def __getitem__(self, slctup: typing.Tuple[typing.Union[slice, int], str]):
        """Returns the aggregated surprisal over a character

        Args:
            slctup (typing.Tuple[typing.Union[slice, int], str]):
                `(slc, slctype) = slctup`: a tuple of a `slc` (slice) and a `slctype` (str).
                `slc` gives the slice of the original string we want to aggregate surprisal over.
                `slctype` indicates if it should be a "char" slice or a "word" slice.
                if a character falls inside a token, then that entire token is included.

        Returns:
            float: the aggregated surprisal over the word span
        """
        try:
            slc, slctype = slctup
            if slctype not in ("word", "char"):
                raise ValueError(f"unrecognized slice type {slctype}")
        except TypeError:
            slc, slctype = slctup, "char"

        if slctype == "char":
            fn = partial(pick_matching_token_ixs, span_type="char")
        elif slctype == "word":
            fn = partial(pick_matching_token_ixs, span_type="word")

        if type(slc) is int:
            slc = slice(slc, slc + 1)

        token_slc = fn(self._tokens, slc)
        return SurprisalQuantity(
            self.surprisals[token_slc].sum(), " ".join(self.tokens[token_slc])
        )

    def __repr__(self) -> str:
        numfmt = "{: >10.3f}"
        strfmt = "{: >10}"
        accumulator = ""
        for t in self.tokens:
            accumulator += strfmt.format(t[:10]) + " "
        accumulator += "\n"
        for s in self.surprisals:
            accumulator += numfmt.format(s) + " "
        return accumulator


class HuggingFaceModel(Model):
    def __init__(self, model_id: str, model_class: typing.Callable) -> None:
        super().__init__(model_id)

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        # self.model_class = model_class
        self.model: PreTrainedModel = model_class.from_pretrained(self.model_id)
        self.model.eval()

    def tokenize(self, textbatch: typing.Union[typing.List, str], max_length=1024):
        if type(textbatch) is str:
            textbatch = [textbatch]

        tokenized = self.tokenizer(
            textbatch,
            padding="longest",
            max_length=max_length,
            return_tensors="pt",
            add_special_tokens=True,
        )

        return tokenized

    @abstractmethod
    def surprise(
        self, textbatch: typing.Union[typing.List, str]
    ) -> HuggingFaceSurprisal:
        raise NotImplementedError

    def extract_surprisal(
        self,
        phrases: typing.Union[str, typing.Collection[str]] = None,
        prefix="",
        suffix="",
    ) -> float:
        """
        Extracts the surprisal of the phrase given the prefix and suffix by making a call to
        `HuggingFaceSurprisal` __getitem__ object. No whitespaces or delimiters are added to
        the prefix or suffix, so make sure to provide an exact string formatted appropriately.
        """
        if type(phrases) is str:
            phrases = [phrases]
        if phrases is None:
            raise ValueError("please provide a phrase to extract the surprisal of")
        textbatch = map(lambda x: str(prefix) + str(x) + str(suffix), phrases)
        slices = map(lambda x: slice(len(prefix), len(prefix + x)), phrases)
        surprisals = self.surprise([*textbatch])
        return [surp[slc, "char"] for surp, slc in zip(surprisals, slices)]


class CausalHuggingFaceModel(HuggingFaceModel):
    def __init__(self, model_id=None) -> None:
        super().__init__(model_id, model_class=AutoModelForCausalLM)

    def surprise(
        self, textbatch: typing.Union[typing.List, str]
    ) -> HuggingFaceSurprisal:
        import torch

        tokenized = self.tokenize(textbatch)

        ids = torch.concat(
            (
                torch.tensor([self.tokenizer.bos_token_id])
                .view(1, -1)
                .repeat(tokenized.input_ids.shape[0], 1),
                tokenized.input_ids,
            ),
            dim=1,
        )

        with torch.no_grad():
            output = self.model(
                ids,
                return_dict=True,
            )

        # b, n, V
        logits = output["logits"]
        # we don't want the pad token to shift the probability distribution,
        # so we set its weight to -inf
        logits[:, :, self.tokenizer.pad_token_id] = -float("inf")
        logsoftmax = torch.log_softmax(logits, dim=2)

        # for CausalLMs, we pick one before the current word to get surprisal of the current word in
        # context of the previous word. otherwise we would be reading off the surprisal of current
        # word given the current word plus context, which would always be high.
        logprobs = (
            logsoftmax[:, :-1, :].gather(2, tokenized.input_ids.unsqueeze(2)).squeeze(2)
        )

        # b stands for an individual item in the batch; each sentence is one item
        # since this is an autoregressive model
        accumulator = []
        for b in range(logprobs.shape[0]):
            accumulator += [
                HuggingFaceSurprisal(
                    tokens=tokenized[b], surprisals=-logprobs[b, :].numpy()
                )
            ]
        return accumulator


class MaskedHuggingFaceModel(HuggingFaceModel):
    def __init__(self, model_id=None) -> None:
        super().__init__(model_id, model_class=AutoModelForMaskedLM)

    def surprise(
        self,
        textbatch: typing.Union[typing.List, str],
        bidirectional=False,
        fixed_length=False,
    ) -> HuggingFaceSurprisal:
        import torch

        tokenized = self.tokenize(textbatch)

        # BERT-like tokenizers already include a bos token in the tokenized sequence with
        # `include_special_tokens=True`
        ids_with_bos_token = tokenized.input_ids
        b, n = ids_with_bos_token.shape
        # new shape: b * n, n
        ids_with_bos_token = ids_with_bos_token.repeat(1, n - 1).view(b * (n - 1), n)
        mask_mask = torch.eye(n, n)[1:, :].repeat(b, 1).bool()
        ids_with_bos_token[mask_mask] = self.tokenizer.mask_token_id

        raise NotImplementedError


class AutoHuggingFaceModel(Model):
    """
    Factory class for initializing surprisal models based on HuggingFace transformers
    """

    def __init__(self) -> None:
        """
        this `__init__` method does nothing; the correct way to use this
        class is using the `from_pretrained` classmethod.
        """

    @classmethod
    def from_pretrained(cls, model_id, model_class: str = None) -> HuggingFaceModel:

        model_class = model_class or ""
        if "gpt" in model_class.lower() + " " + model_id.lower():
            model_class = AutoModelForCausalLM
            hfm = CausalHuggingFaceModel(model_id)
            # for GPT-like tokenizers, pad token is not set as it is generally inconsequential for autoregressive models
            hfm.tokenizer.pad_token = hfm.tokenizer.eos_token
            return hfm
        elif "bert" in model_class.lower() + " " + model_id.lower():
            model_class = AutoModelForMaskedLM
            hfm = MaskedHuggingFaceModel(model_id)
            return hfm
        else:
            raise ValueError(
                f"unable to determine appropriate model class based for model_id="
                f'"{model_id}" and model_class="{model_class}". '
                f'Please explicitly pass either "gpt" or "bert" as model_class.'
            )
