from pathlib import Path

from yet_another_imod_wrapper.fiducials import generate_alignment_directive
from yet_another_imod_wrapper.patch_tracking import generate_patch_tracking_alignment_directive


def test_patch_tracking_directive_generation():
    """Check that patch tracking directive is properly generated."""
    directive = generate_patch_tracking_alignment_directive(
        tilt_series_file=Path('test.mrc'),
        pixel_size=1.05,
        rotation_angle=45.5,
        patch_size_xy=(50, 100),
        patch_overlap_percentage=33
    )
    assert directive == {
        'setupset.copyarg.userawtlt': '1', 'setupset.copyarg.stackext': '.mrc',
        'setupset.copyarg.rotation': str(45.5),
        'setupset.copyarg.pixel': str(1.05 / 10),
        'setupset.copyarg.gold': '10', 'setupset.copyarg.dual': '0',
        'runtime.Positioning.any.wholeTomogram': '1',
        'runtime.PatchTracking.any.adjustTiltAngles': '0',
        'runtime.Fiducials.any.trackingMethod': '1',
        'runtime.Fiducials.any.seedingMethod': '3',
        'runtime.Excludeviews.any.deleteOldFiles': '0',
        'runtime.AlignedStack.any.binByFactor': '8',
        'comparam.xcorr_pt.tiltxcorr.SizeOfPatchesXandY': '6,12',
        'comparam.xcorr_pt.tiltxcorr.OverlapOfPatchesXandY': '0.33,0.33',
        'comparam.xcorr_pt.tiltxcorr.ShiftLimitsXandY': '200,200',
        'comparam.xcorr_pt.tiltxcorr.LengthAndOverlap': '16,4',
        'comparam.xcorr_pt.tiltxcorr.IterateCorrelations': '20',
        'comparam.xcorr_pt.tiltxcorr.FilterSigma2': '0.03',
        'comparam.xcorr_pt.tiltxcorr.FilterRadius2': '0.125',
        'comparam.track.beadtrack.SobelFilterCentering': '1',
        'comparam.track.beadtrack.ScalableSigmaForSobel': '0.12',
        'comparam.tilt.tilt.THICKNESS': '3000',
        'comparam.prenewst.newstack.BinByFactor': str(8),
        'comparam.prenewst.newstack.AntialiasFilter': '-1',
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


def test_fiducial_directive_generation():
    """Check that fiducial based alignment directive is properly generated."""
    directive = generate_alignment_directive(
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
