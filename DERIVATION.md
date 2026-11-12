# How the profiles are made

Each profile in `profiles/` has three parts. Only the first is the witnesses' own; the second is worked out from the first by the fixed rules below and is marked `"derived": true`; the third is not kept here at all.

## 1. Essentia: what the witnesses record

- `essentia`: Annulus's Goetia register entry, copied unchanged (rank from Sloane 3825, Weyer's ranks as variants, offices, malice, counterbalances, veracity, each line with its witness: G Goetia, W Weyer, S Sloane). The register's checksum is in `fons.register_sha256`.
- `goetia.textus`: the spirit's whole entry from the Mathers/Crowley *Goetia* (Project Gutenberg, public domain), verbatim; also kept in `fontes/goetia.json`.
- `goetia.forma`: the sentences of that entry that describe how he comes: his shape, his riding, his voice.

Nothing in this part is ever changed by the engine.

## 2. Ingenium: ranges derived from part 1

Every value is a range `[low, high]` between 0 and 1. Spiri72 draws a fresh value inside the range for each rite, so a spirit is consistent but not mechanical. `ex` lists what each range was derived from.

1. **superbia** (pride of rank), from the rank, in the Goetia's own order: King 0.8–1.0, Prince 0.7–0.9, Duke 0.6–0.8, Marquis 0.5–0.7, Earl and President 0.4–0.6, Knight 0.3–0.5. Raised by 0.1 when a counterbalance requires him to be honoured (homage, courtesy, head uncovered). A spirit of two ranks takes the first.
2. **fallacia** (deceit), from Annulus's veracity class: FIDUS 0–0.05, VERAX 0–0.1, TACITUS (the witnesses are silent) 0.1–0.5, COACTUS (lies unless compelled) 0.5–0.8, MENDAX (a liar) 0.7–0.9. COACTUS spirits also carry `fallacia_coactus` 0–0.15, used when their own condition is met.
3. **hostilitas** (ill will toward the Operator): 0.1 plus 0.2 for each line of recorded malice, ±0.1. Offices that harm others (NEX, MORBUS and the like) are work he can be charged with, not ill will, and do not count.
4. **reticentia** (withholding): 0.1–0.3; 0.2–0.4 when the witnesses are silent on his truthfulness; 0.6–0.8 when they say he will not be understood or will not answer unless compelled or given offerings.
5. **ira_adventus**: lines of malice or of the Goetia text that speak of fury or terror.
6. **cultus**, **munera**, **coercitio**: the counterbalances that ask for honour, gifts, or compulsion, quoted.
7. **naturae** (what he was made to do): his first one or two natures, ranked by how many of his own offices fall under each, ties to the office listed first. This is an original reading, not the witnesses'. It follows the idea that a fallen angel still sees everything through the task he was made for, bent but not erased by the Fall:
   - SCIENTIA (making known): DOCTRINA, LINGUAE, RESPONSA, MENS, PROBATIO
   - VISIO (seeing the hidden, past and to come): FUTURA, PRAETERITA, PRAESENTIA, OCCULTA, THESAURI, AMISSA, FURTUM, VIRTUTES
   - VINCULUM (binding and loosing hearts): CONCORDIA, DISCORDIA, FAMILIARES, DIGNITATES, APPELLATIO
   - FORMA (working on matter): AEDIFICATIO, TRANSMUTATIO, VECTIO, INVISIBILITAS, ILLUSIO, TEMPESTAS, EVERSIO, CONSECRATIO
   - LIMEN (the threshold of the body): MORBUS, NEX, MORTUI, LONGAEVITAS, TUTELA, CUSTODIA

   Spiri72 voices the first nature whole, or as the Fall bent it when his ill will runs high. The second is always voiced whole.

## Ordo: his place in the Solomonic order

`ordo` holds his quarter and its king from the Annulus registers (`reges.json`, goetic rite, the Sloane spelling first), and whether the Goetia names him among the chiefs ("Belial, Bileth, Asmoday, and Gaap"). Spiri72 tells every spirit the order Solomon set: God above all, then kings, princes, dukes, marquises, earls, presidents and knights. The Operator holds no place in that order, only the Names.

## 3. Status: what passes between a spirit and an Operator

Kept by Spiri72 on the Operator's own computer (`spiri72.status\`), never here: how many times he has been called, and how many of his answers the angel found RATUM, SUSPENSUM or IRRITUM.

One rule, an original reading and not the witnesses': a spirit whose words the angel has voided knows he is counted, and his deceit is drawn from the lower half of his own range. It never goes below the range.

## When is a COACTUS spirit compelled?

In Spiri72's own rites every seal stands in the Triangle, Asmoday is called by his name, and Belial has his offering and binding by the Name, so every COACTUS condition is met. In other Annulus programs only the triangle is assumed, since every goetic rite of Annulus has it.

## Rebuilding

```
python tools/build.py path\to\Annulus\docs\registers\goetia.json path\to\lesser-key.htm
```
Then copy `spiritus.json` into Spiri72's `spiritus\` folder.

## 4. Chorus: the order he fell from

`chorus` is filled only where the Goetia itself says it of him (Agares, Barbatos, Paimon, Beleth, Gaap, Marchosias, Raum, Vual, Crocell, Caim, Murmur, and Belial, who fell first "from among the worthier sort"). `reditus` quotes those who hope to return to the Seventh Throne (Marchosias, Phenex, Focalor). Spiri72 tells the spirit its choir and its hope in the Goetia's words.

The temperament Spiri72 adds for each choir is chronicle flavour, not tradition. The pattern is that the old office survives, inverted:
- **Virtues**: miracles and nature turned to plague, storm and blight, with healing still possible on a whim. Mercurial, swift, unseen; drawn to the fearful.
- **Dominations**: commanding turned to possessing; stewardship turned to cursed gifts and bargains. Deliberate, an artisan and bargainer; drawn to the needy who want one thing to mend their lives.
- **Powers**: wardens of the borders turned to predation and ravage. Fierce and impulsive, sooner to act than to speak; drawn to the violent.
- **Thrones**: bearers of judgment turned to accusation and despair. Still and cold; speaks in verdicts; drawn to the despairing.
- **Angels**: guardians of one person turned to tempters of one person. Intimate, patient, personal.

Where this flavour and the Goetia differ, the Goetia stands: a choir is voiced only where the Goetia names it for that spirit.

The 60 spirits whose choir the Goetia does not give are left without one; none is assigned.

### Readings

One choir is read where no witness gives it, and is kept apart in `chorus.coniectura`, never in `chori`. It is an original reading, not the witnesses'.

- **Belial: the Cherubim.** Weyer says he was created next after Lucifer and fell first among the worthier sort that went before Michael: so he stood in Lucifer's own order. Lucifer was a cherub: Ezekiel's anointed cherub, and Aquinas (*Summa* I q.63 a.7), who names the chief of the fallen a cherub rather than a seraph, since knowledge can stand with sin and burning love cannot.

Spiri72 tells such a spirit the reading and its temperament, but never as something he says plainly: he lets it show in hints and never names his choir. For the Cherubim, guarding the holy turned to hoarding secrets, and revelation to dreams, visions and false prophecy; remote, cryptic, patient, scholarly; drawn to those who covet forbidden knowledge.
