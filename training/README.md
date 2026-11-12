# Training set

`spiri72.jsonl` holds 798 examples, one per line, in the common chat format (`messages` with system, user and assistant). Every example uses exactly the prompts Spiri72 sends, including the spirit engine's brief, and every answer passes Spiri72's own reader. Where the angel can check an answer, the generator checks it too before writing it.

| kind | count | what it teaches |
|---|---|---|
| `persona` | 288 (4 per spirit) | naming himself, his rank, his coming and his offices from the witnesses' words, in the voice his brief gives |
| `virtutes` | 240 (the 8 spirits with that office) | counting handed texts exactly as the angel counts them, whatever his bearing |
| `praeterita` | 270 (the 18 spirits with that office) | recounting the record line for line, whole or in part, never inventing |

Each line's `meta` says which spirit, which kind, and which outcome. The opening lines of `persona` answers come from a small set of templates (`"voice": "templated"`). The facts in them are the register's and the Goetia's.

This is a seed set. It teaches form and honesty well, but it doesn't give each spirit a voice of his own. That should come from real rites the angel has passed.

To remake it after the profiles change:
```
spiri72.exe --exempla spiri72.jsonl
```

## Fine-tuning (a LoRA)

A LoRA is a small add-on file that changes how the model behaves without replacing it. Training one needs a graphics card. An NVIDIA card with 12 GB or more works on your own computer. Otherwise use a free cloud notebook such as Google Colab.

1. Use the same base model you run in llama-server (for example Qwen3 8B), in its original form from Hugging Face, not the GGUF file.
2. Train a LoRA on `spiri72.jsonl` with a tool such as Unsloth or Axolotl (both read this chat format). Start small: rank 16, 1 to 2 passes over the data. Too much training makes every spirit sound alike.
3. Export the LoRA to GGUF. Unsloth can do this itself, or use llama.cpp's `convert_lora_to_gguf.py`.
4. Start the model with it:
   ```
   llama-server.exe -m path\to\model.gguf --lora path\to\spiri72-lora.gguf --port 8080 -c 8192
   ```
5. Test it: bind Bathin or Stolas and hand them a file. The angel's recount tells you straight away whether the model still counts true.

The LoRA, like the control vectors, changes only how a spirit speaks and answers. What it may do stays in Annulus.
