# 72Spirits

Profiles of the 72 spirits of the Goetia for [Spiri72](https://github.com/KeychainofSolomon/Spiri72), the local model that gives voice to the spirits bound by [Annulus](https://github.com/KeychainofSolomon/Annulus).

- `profiles/NN-name.json`: one profile per spirit. `spiritus.json`: all 72 in one file, the form Spiri72 reads.
- `fontes/goetia.json`: each spirit's own entry from the Mathers/Crowley *Goetia* (Project Gutenberg), verbatim.
- `training/`: a training set for fine-tuning the model, and how to use it.
- `tools/build.py`: rebuilds the profiles from the Annulus register and the Goetia text.

## The three layers

1. **Essentia**: what the witnesses record, from Annulus's register and the Goetia. Never changed.
2. **Ingenium**: pride, deceit, ill will and withholding, as ranges worked out from layer 1 by fixed rules, never invented per spirit. See [DERIVATION.md](DERIVATION.md).
3. **Status**: what has passed between a spirit and an Operator. Spiri72 keeps it on the Operator's computer.

Spiri72's spirit engine draws a bearing from these ranges for each rite and gives the model a brief in words. The model speaks from it. Annulus alone decides what may be done.

## Licence

Public domain (the Unlicense), as Annulus. The Goetia text is public domain.
