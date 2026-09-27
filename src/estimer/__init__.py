"""Estimator: any electrical plan PDF -> symbol counts per family per sheet,
in the format of the human estimator's (M. Dupuis) Plan Expert takeoffs.

Entry points:
  python -m src.estimer <any.pdf> [--out DIR]      one-shot estimate
  python -m src.estimer.evaluate                   leave-one-out vs Dupuis

Everything the detector knows is learnt from the Dupuis reference takeoffs
(`dossiers/S-*/reference/*Dupuis*.qpl`) through `src.estimer.train`; nothing is
hard-coded per dossier.
"""
