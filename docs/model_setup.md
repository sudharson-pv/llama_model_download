# Model Setup and Export Guide

This document explains how ExecuTorch PTE model files and tokenizers are prepared for LearnMate AI.

## 1. Prerequisites
- Python 3.10+
- PyTorch 2.4.0+
- ExecuTorch 1.4.0
- Hugging Face Transformers
- `executorch.backends.xnnpack`

## 2. Model Export Flow
To export Meta Llama 3.2 1B Instruct:
1. Clone the model from Hugging Face or Meta (requires Meta Llama 3.2 Community License agreement).
2. Quantize model weights using dynamic int8 activation and int4 weight quantization (`8da4w`) with group size 32.
3. Export the model using `torch.export.export()` and the ExecuTorch XNNPACK backend.
4. Save the compiled program to `llama3_2_1b_8da4w.pte`.
5. Extract `tokenizer.model` (2,183,982 bytes).

## 3. Mandatory Invariants
- Format must be ExecuTorch PTE. Never rename GGUF files to PTE.
- The first 4 bytes must not match `GGUF` (`0x47 0x47 0x55 0x46`).
- Always calculate SHA-256 and exact byte size using `scripts/calculate_hashes.py`.
