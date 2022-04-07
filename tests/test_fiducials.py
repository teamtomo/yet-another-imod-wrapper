from pathlib import Path

from yet_another_imod_wrapper.fiducials import generate_fiducial_alignment_directive


def test_alignment_directive_generation():
    """Check that fiducial based alignment directive is properly generated."""
    directive = generate_fiducial_alignment_directive(
        tilt_series_file=Path('test.mrc'),
        pixel_size=1.05,
        fiducial_size=10,
        rotation_angle=85.5
    )
    assert directive == {
        'setupset.copyarg.userawtlt': '1',
        'setupset.copyarg.stackext': '.mrc',
        'setupset.copyarg.rotation': str(85.5),
        'setupset.copyarg.pixel': str(1.05 / 10),
        'setupset.copyarg.gold': str(10),
        'setupset.copyarg.dual': '0',
        'runtime.Positioning.any.wholeTomogram': '1',
        'runtime.Fiducials.any.trackingMethod': '0',
        'runtime.Fiducials.any.seedingMethod': '3',
        'runtime.Excludeviews.any.deleteOldFiles': '0',
        'runtime.AlignedStack.any.binByFactor': '8',
        'comparam.prenewst.newstack.BinByFactor': str(8),
        'comparam.prenewst.newstack.AntialiasFilter': '-1',
        'comparam.autofidseed.autofidseed.TargetNumberOfBeads': '50',
        'comparam.track.beadtrack.SobelFilterCentering': '1',
        'comparam.track.beadtrack.ScalableSigmaForSobel': '0.12',
        'comparam.newst.newstack.TaperAtFill': '1,1',
        'comparam.newst.newstack.AntialiasFilter': '-1',
        'comparam.golderaser.ccderaser.ExpandCircleIterations': '3',
        'comparam.eraser.ccderaser.PeakCriterion': '8.0',
        'comparam.eraser.ccderaser.DiffCriterion': '6.0',
        'comparam.align.tiltalign.TiltOption': '0',
        'comparam.align.tiltalign.SurfacesToAnalyze': '1',
        'comparam.align.tiltalign.RotOption': '-1',
        'comparam.align.tiltalign.MagOption': '0',
        'comparam.align.tiltalign.BeamTiltOption': '2'
    }
