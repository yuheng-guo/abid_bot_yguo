# Visit 3.1.4 log file
ScriptVersion = "3.1.4"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
OpenDatabase("/anvil/scratch/x-yguo11/bhdisk_sol_05/h5data/3d_data_26_04_09_080010/rho_b.file_* database", 0)
# The UpdateDBPluginInfo RPC is not supported in the VisIt module so it will not be logged.
DefineScalarExpression("operators/ConnectedComponents/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0.)")
DefineCurveExpression("operators/DataBinning/1D/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/DataBinning/2D/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/DataBinning/3D/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/Flux/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0.)")
DefineCurveExpression("operators/Lineout/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/ModelFit/model", "point_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/ModelFit/distance", "point_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/StatisticalTrends/Sum/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Mean/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Variance/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Std. Dev./MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Slope/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Residuals/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineVectorExpression("operators/SurfaceNormal/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0.)")
DefineScalarExpression("rho_b", "conn_cmfe(</anvil/scratch/x-yguo11/bhdisk_sol_05/h5data/3d_data_26_04_09_080010/rho_b.file_* database[0]id:MHD_EVOLVE--rho_b>, <Carpet AMR-grid>)")
DefineScalarExpression("operators/ConnectedComponents/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0.)")
DefineCurveExpression("operators/DataBinning/1D/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/DataBinning/2D/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/DataBinning/3D/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/Flux/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0.)")
DefineCurveExpression("operators/Lineout/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/ModelFit/model", "point_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/ModelFit/distance", "point_constant(<Carpet AMR-grid>, 0)")
DefineScalarExpression("operators/StatisticalTrends/Sum/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Mean/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Variance/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Std. Dev./MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Slope/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineScalarExpression("operators/StatisticalTrends/Residuals/MHD_EVOLVE--rho_b", "cell_constant(<MHD_EVOLVE--rho_b>, 0.)")
DefineVectorExpression("operators/SurfaceNormal/Carpet AMR-grid", "cell_constant(<Carpet AMR-grid>, 0.)")
DefineScalarExpression("rho_b", "conn_cmfe(</anvil/scratch/x-yguo11/bhdisk_sol_05/h5data/3d_data_26_04_09_080010/rho_b.file_* database[0]id:MHD_EVOLVE--rho_b>, <Carpet AMR-grid>)")
DefineScalarExpression("logrho", "log10(<MHD_EVOLVE--rho_b>/0.000461833107670726)")
OpenDatabase("/anvil/scratch/x-yguo11/bhdisk_sol_05/xml/3d_data_26_04_09_080010/bh1_*.3d database", 0)
OpenDatabase("/anvil/scratch/x-yguo11/bhdisk_sol_05/xml/3d_data_26_04_09_080010/spin_*.vtk database", 0)
CreateDatabaseCorrelation("Everything",("/anvil/scratch/x-yguo11/bhdisk_sol_05/h5data/3d_data_26_04_09_080010/rho_b.file_* database", "/anvil/scratch/x-yguo11/bhdisk_sol_05/xml/3d_data_26_04_09_080010/bh1_*.3d database", "/anvil/scratch/x-yguo11/bhdisk_sol_05/xml/3d_data_26_04_09_080010/spin_*.vtk database"), 0)
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 1
AnnotationAtts.axes2D.autoSetTicks = 1
AnnotationAtts.axes2D.autoSetScaling = 1
AnnotationAtts.axes2D.lineWidth = 0
AnnotationAtts.axes2D.tickLocation = AnnotationAtts.axes2D.Outside  # Inside, Outside, Both
AnnotationAtts.axes2D.tickAxes = AnnotationAtts.axes2D.BottomLeft  # Off, Bottom, Left, BottomLeft, All
AnnotationAtts.axes2D.xAxis.title.visible = 1
AnnotationAtts.axes2D.xAxis.title.font.font = AnnotationAtts.axes2D.xAxis.title.font.Courier  # Arial, Courier, Times
AnnotationAtts.axes2D.xAxis.title.font.scale = 1
AnnotationAtts.axes2D.xAxis.title.font.useForegroundColor = 1
AnnotationAtts.axes2D.xAxis.title.font.color = (0, 0, 0, 255)
AnnotationAtts.axes2D.xAxis.title.font.bold = 1
AnnotationAtts.axes2D.xAxis.title.font.italic = 1
AnnotationAtts.axes2D.xAxis.title.userTitle = 0
AnnotationAtts.axes2D.xAxis.title.userUnits = 0
AnnotationAtts.axes2D.xAxis.title.title = "X-Axis"
AnnotationAtts.axes2D.xAxis.title.units = ""
AnnotationAtts.axes2D.xAxis.label.visible = 1
AnnotationAtts.axes2D.xAxis.label.font.font = AnnotationAtts.axes2D.xAxis.label.font.Courier  # Arial, Courier, Times
AnnotationAtts.axes2D.xAxis.label.font.scale = 1
AnnotationAtts.axes2D.xAxis.label.font.useForegroundColor = 1
AnnotationAtts.axes2D.xAxis.label.font.color = (0, 0, 0, 255)
AnnotationAtts.axes2D.xAxis.label.font.bold = 1
AnnotationAtts.axes2D.xAxis.label.font.italic = 1
AnnotationAtts.axes2D.xAxis.label.scaling = 0
AnnotationAtts.axes2D.xAxis.tickMarks.visible = 1
AnnotationAtts.axes2D.xAxis.tickMarks.majorMinimum = 0
AnnotationAtts.axes2D.xAxis.tickMarks.majorMaximum = 1
AnnotationAtts.axes2D.xAxis.tickMarks.minorSpacing = 0.02
AnnotationAtts.axes2D.xAxis.tickMarks.majorSpacing = 0.2
AnnotationAtts.axes2D.xAxis.grid = 0
AnnotationAtts.axes2D.yAxis.title.visible = 1
AnnotationAtts.axes2D.yAxis.title.font.font = AnnotationAtts.axes2D.yAxis.title.font.Courier  # Arial, Courier, Times
AnnotationAtts.axes2D.yAxis.title.font.scale = 1
AnnotationAtts.axes2D.yAxis.title.font.useForegroundColor = 1
AnnotationAtts.axes2D.yAxis.title.font.color = (0, 0, 0, 255)
AnnotationAtts.axes2D.yAxis.title.font.bold = 1
AnnotationAtts.axes2D.yAxis.title.font.italic = 1
AnnotationAtts.axes2D.yAxis.title.userTitle = 0
AnnotationAtts.axes2D.yAxis.title.userUnits = 0
AnnotationAtts.axes2D.yAxis.title.title = "Y-Axis"
AnnotationAtts.axes2D.yAxis.title.units = ""
AnnotationAtts.axes2D.yAxis.label.visible = 1
AnnotationAtts.axes2D.yAxis.label.font.font = AnnotationAtts.axes2D.yAxis.label.font.Courier  # Arial, Courier, Times
AnnotationAtts.axes2D.yAxis.label.font.scale = 1
AnnotationAtts.axes2D.yAxis.label.font.useForegroundColor = 1
AnnotationAtts.axes2D.yAxis.label.font.color = (0, 0, 0, 255)
AnnotationAtts.axes2D.yAxis.label.font.bold = 1
AnnotationAtts.axes2D.yAxis.label.font.italic = 1
AnnotationAtts.axes2D.yAxis.label.scaling = 0
AnnotationAtts.axes2D.yAxis.tickMarks.visible = 1
AnnotationAtts.axes2D.yAxis.tickMarks.majorMinimum = 0
AnnotationAtts.axes2D.yAxis.tickMarks.majorMaximum = 1
AnnotationAtts.axes2D.yAxis.tickMarks.minorSpacing = 0.02
AnnotationAtts.axes2D.yAxis.tickMarks.majorSpacing = 0.2
AnnotationAtts.axes2D.yAxis.grid = 0
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.axes3D.autoSetTicks = 1
AnnotationAtts.axes3D.autoSetScaling = 1
AnnotationAtts.axes3D.lineWidth = 0
AnnotationAtts.axes3D.tickLocation = AnnotationAtts.axes3D.Inside  # Inside, Outside, Both
AnnotationAtts.axes3D.axesType = AnnotationAtts.axes3D.ClosestTriad  # ClosestTriad, FurthestTriad, OutsideEdges, StaticTriad, StaticEdges
AnnotationAtts.axes3D.triadFlag = 0
AnnotationAtts.axes3D.bboxFlag = 0
AnnotationAtts.axes3D.xAxis.title.visible = 1
AnnotationAtts.axes3D.xAxis.title.font.font = AnnotationAtts.axes3D.xAxis.title.font.Arial  # Arial, Courier, Times
AnnotationAtts.axes3D.xAxis.title.font.scale = 1
AnnotationAtts.axes3D.xAxis.title.font.useForegroundColor = 1
AnnotationAtts.axes3D.xAxis.title.font.color = (0, 0, 0, 255)
AnnotationAtts.axes3D.xAxis.title.font.bold = 0
AnnotationAtts.axes3D.xAxis.title.font.italic = 0
AnnotationAtts.axes3D.xAxis.title.userTitle = 0
AnnotationAtts.axes3D.xAxis.title.userUnits = 0
AnnotationAtts.axes3D.xAxis.title.title = "X-Axis"
AnnotationAtts.axes3D.xAxis.title.units = ""
AnnotationAtts.axes3D.xAxis.label.visible = 1
AnnotationAtts.axes3D.xAxis.label.font.font = AnnotationAtts.axes3D.xAxis.label.font.Arial  # Arial, Courier, Times
AnnotationAtts.axes3D.xAxis.label.font.scale = 1
AnnotationAtts.axes3D.xAxis.label.font.useForegroundColor = 1
AnnotationAtts.axes3D.xAxis.label.font.color = (0, 0, 0, 255)
AnnotationAtts.axes3D.xAxis.label.font.bold = 0
AnnotationAtts.axes3D.xAxis.label.font.italic = 0
AnnotationAtts.axes3D.xAxis.label.scaling = 0
AnnotationAtts.axes3D.xAxis.tickMarks.visible = 1
AnnotationAtts.axes3D.xAxis.tickMarks.majorMinimum = 0
AnnotationAtts.axes3D.xAxis.tickMarks.majorMaximum = 1
AnnotationAtts.axes3D.xAxis.tickMarks.minorSpacing = 0.02
AnnotationAtts.axes3D.xAxis.tickMarks.majorSpacing = 0.2
AnnotationAtts.axes3D.xAxis.grid = 0
AnnotationAtts.axes3D.yAxis.title.visible = 1
AnnotationAtts.axes3D.yAxis.title.font.font = AnnotationAtts.axes3D.yAxis.title.font.Arial  # Arial, Courier, Times
AnnotationAtts.axes3D.yAxis.title.font.scale = 1
AnnotationAtts.axes3D.yAxis.title.font.useForegroundColor = 1
AnnotationAtts.axes3D.yAxis.title.font.color = (0, 0, 0, 255)
AnnotationAtts.axes3D.yAxis.title.font.bold = 0
AnnotationAtts.axes3D.yAxis.title.font.italic = 0
AnnotationAtts.axes3D.yAxis.title.userTitle = 0
AnnotationAtts.axes3D.yAxis.title.userUnits = 0
AnnotationAtts.axes3D.yAxis.title.title = "Y-Axis"
AnnotationAtts.axes3D.yAxis.title.units = ""
AnnotationAtts.axes3D.yAxis.label.visible = 1
AnnotationAtts.axes3D.yAxis.label.font.font = AnnotationAtts.axes3D.yAxis.label.font.Arial  # Arial, Courier, Times
AnnotationAtts.axes3D.yAxis.label.font.scale = 1
AnnotationAtts.axes3D.yAxis.label.font.useForegroundColor = 1
AnnotationAtts.axes3D.yAxis.label.font.color = (0, 0, 0, 255)
AnnotationAtts.axes3D.yAxis.label.font.bold = 0
AnnotationAtts.axes3D.yAxis.label.font.italic = 0
AnnotationAtts.axes3D.yAxis.label.scaling = 0
AnnotationAtts.axes3D.yAxis.tickMarks.visible = 1
AnnotationAtts.axes3D.yAxis.tickMarks.majorMinimum = 0
AnnotationAtts.axes3D.yAxis.tickMarks.majorMaximum = 1
AnnotationAtts.axes3D.yAxis.tickMarks.minorSpacing = 0.02
AnnotationAtts.axes3D.yAxis.tickMarks.majorSpacing = 0.2
AnnotationAtts.axes3D.yAxis.grid = 0
AnnotationAtts.axes3D.zAxis.title.visible = 1
AnnotationAtts.axes3D.zAxis.title.font.font = AnnotationAtts.axes3D.zAxis.title.font.Arial  # Arial, Courier, Times
AnnotationAtts.axes3D.zAxis.title.font.scale = 1
AnnotationAtts.axes3D.zAxis.title.font.useForegroundColor = 1
AnnotationAtts.axes3D.zAxis.title.font.color = (0, 0, 0, 255)
AnnotationAtts.axes3D.zAxis.title.font.bold = 0
AnnotationAtts.axes3D.zAxis.title.font.italic = 0
AnnotationAtts.axes3D.zAxis.title.userTitle = 0
AnnotationAtts.axes3D.zAxis.title.userUnits = 0
AnnotationAtts.axes3D.zAxis.title.title = "Z-Axis"
AnnotationAtts.axes3D.zAxis.title.units = ""
AnnotationAtts.axes3D.zAxis.label.visible = 1
AnnotationAtts.axes3D.zAxis.label.font.font = AnnotationAtts.axes3D.zAxis.label.font.Arial  # Arial, Courier, Times
AnnotationAtts.axes3D.zAxis.label.font.scale = 1
AnnotationAtts.axes3D.zAxis.label.font.useForegroundColor = 1
AnnotationAtts.axes3D.zAxis.label.font.color = (0, 0, 0, 255)
AnnotationAtts.axes3D.zAxis.label.font.bold = 0
AnnotationAtts.axes3D.zAxis.label.font.italic = 0
AnnotationAtts.axes3D.zAxis.label.scaling = 0
AnnotationAtts.axes3D.zAxis.tickMarks.visible = 1
AnnotationAtts.axes3D.zAxis.tickMarks.majorMinimum = 0
AnnotationAtts.axes3D.zAxis.tickMarks.majorMaximum = 1
AnnotationAtts.axes3D.zAxis.tickMarks.minorSpacing = 0.02
AnnotationAtts.axes3D.zAxis.tickMarks.majorSpacing = 0.2
AnnotationAtts.axes3D.zAxis.grid = 0
AnnotationAtts.axes3D.setBBoxLocation = 0
AnnotationAtts.axes3D.bboxLocation = (0, 1, 0, 1, 0, 1)
AnnotationAtts.axes3D.triadColor = (0, 0, 0)
AnnotationAtts.axes3D.triadLineWidth = 1
AnnotationAtts.axes3D.triadFont = 0
AnnotationAtts.axes3D.triadBold = 1
AnnotationAtts.axes3D.triadItalic = 1
AnnotationAtts.axes3D.triadSetManually = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.userInfoFont.font = AnnotationAtts.userInfoFont.Arial  # Arial, Courier, Times
AnnotationAtts.userInfoFont.scale = 1
AnnotationAtts.userInfoFont.useForegroundColor = 1
AnnotationAtts.userInfoFont.color = (0, 0, 0, 255)
AnnotationAtts.userInfoFont.bold = 0
AnnotationAtts.userInfoFont.italic = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 1
AnnotationAtts.databaseInfoFont.font = AnnotationAtts.databaseInfoFont.Arial  # Arial, Courier, Times
AnnotationAtts.databaseInfoFont.scale = 1
AnnotationAtts.databaseInfoFont.useForegroundColor = 1
AnnotationAtts.databaseInfoFont.color = (0, 0, 0, 255)
AnnotationAtts.databaseInfoFont.bold = 0
AnnotationAtts.databaseInfoFont.italic = 0
AnnotationAtts.databaseInfoExpansionMode = AnnotationAtts.File  # File, Directory, Full, Smart, SmartDirectory
AnnotationAtts.databaseInfoTimeScale = 1
AnnotationAtts.databaseInfoTimeOffset = 0
AnnotationAtts.legendInfoFlag = 0
AnnotationAtts.backgroundColor = (55, 118, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
AnnotationAtts.gradientBackgroundStyle = AnnotationAtts.Radial  # TopToBottom, BottomToTop, LeftToRight, RightToLeft, Radial
AnnotationAtts.gradientColor1 = (0, 0, 255, 255)
AnnotationAtts.gradientColor2 = (0, 0, 0, 255)
AnnotationAtts.backgroundMode = AnnotationAtts.Solid  # Solid, Gradient, Image, ImageSphere
AnnotationAtts.backgroundImage = ""
AnnotationAtts.imageRepeatX = 1
AnnotationAtts.imageRepeatY = 1
AnnotationAtts.axesArray.visible = 1
AnnotationAtts.axesArray.ticksVisible = 1
AnnotationAtts.axesArray.autoSetTicks = 1
AnnotationAtts.axesArray.autoSetScaling = 1
AnnotationAtts.axesArray.lineWidth = 0
AnnotationAtts.axesArray.axes.title.visible = 1
AnnotationAtts.axesArray.axes.title.font.font = AnnotationAtts.axesArray.axes.title.font.Arial  # Arial, Courier, Times
AnnotationAtts.axesArray.axes.title.font.scale = 1
AnnotationAtts.axesArray.axes.title.font.useForegroundColor = 1
AnnotationAtts.axesArray.axes.title.font.color = (0, 0, 0, 255)
AnnotationAtts.axesArray.axes.title.font.bold = 0
AnnotationAtts.axesArray.axes.title.font.italic = 0
AnnotationAtts.axesArray.axes.title.userTitle = 0
AnnotationAtts.axesArray.axes.title.userUnits = 0
AnnotationAtts.axesArray.axes.title.title = ""
AnnotationAtts.axesArray.axes.title.units = ""
AnnotationAtts.axesArray.axes.label.visible = 1
AnnotationAtts.axesArray.axes.label.font.font = AnnotationAtts.axesArray.axes.label.font.Arial  # Arial, Courier, Times
AnnotationAtts.axesArray.axes.label.font.scale = 1
AnnotationAtts.axesArray.axes.label.font.useForegroundColor = 1
AnnotationAtts.axesArray.axes.label.font.color = (0, 0, 0, 255)
AnnotationAtts.axesArray.axes.label.font.bold = 0
AnnotationAtts.axesArray.axes.label.font.italic = 0
AnnotationAtts.axesArray.axes.label.scaling = 0
AnnotationAtts.axesArray.axes.tickMarks.visible = 1
AnnotationAtts.axesArray.axes.tickMarks.majorMinimum = 0
AnnotationAtts.axesArray.axes.tickMarks.majorMaximum = 1
AnnotationAtts.axesArray.axes.tickMarks.minorSpacing = 0.02
AnnotationAtts.axesArray.axes.tickMarks.majorSpacing = 0.2
AnnotationAtts.axesArray.axes.grid = 0
SetAnnotationAttributes(AnnotationAtts)
# Logging for AddAnnotationObject is not implemented yet.
# Logging for SetAnnotationObjectOptions is not implemented yet.
# Logging for SetAnnotationObjectOptions is not implemented yet.
# Logging for SetAnnotationObjectOptions is not implemented yet.
# Logging for SetAnnotationObjectOptions is not implemented yet.
# Logging for SetAnnotationObjectOptions is not implemented yet.
SetActivePlots()
DeleteActivePlots()
ActivateDatabase("/anvil/scratch/x-yguo11/bhdisk_sol_05/h5data/3d_data_26_04_09_080010/rho_b.file_* database")
AddPlot("Pseudocolor", "logrho", 1, 1)
SetActivePlots(0)
ActivateDatabase("/anvil/scratch/x-yguo11/bhdisk_sol_05/xml/3d_data_26_04_09_080010/bh1_*.3d database")
AddPlot("Pseudocolor", "bh1p", 1, 1)
SetActivePlots(1)
AddOperator("Delaunay", 1)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 0
PseudocolorAtts.min = 0
PseudocolorAtts.useBelowMinColor = 0
PseudocolorAtts.belowMinColor = (0, 0, 0, 255)
PseudocolorAtts.maxFlag = 0
PseudocolorAtts.max = 1
PseudocolorAtts.useAboveMaxColor = 0
PseudocolorAtts.aboveMaxColor = (0, 0, 0, 255)
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "gray"
PseudocolorAtts.invertColorTable = 0
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 0
PseudocolorAtts.lightingFlag = 0
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
ActivateDatabase("/anvil/scratch/x-yguo11/bhdisk_sol_05/xml/3d_data_26_04_09_080010/spin_*.vtk database")
AddPlot("Vector", "spinvec", 1, 1)
SetActivePlots(2)
AddOperator("Reflect", 1)
ReflectAtts = ReflectAttributes()
ReflectAtts.octant = ReflectAtts.PXPYPZ  # PXPYPZ, NXPYPZ, PXNYPZ, NXNYPZ, PXPYNZ, NXPYNZ, PXNYNZ, NXNYNZ
ReflectAtts.useXBoundary = 1
ReflectAtts.specifiedX = 0
ReflectAtts.useYBoundary = 1
ReflectAtts.specifiedY = 0
ReflectAtts.useZBoundary = 1
ReflectAtts.specifiedZ = 0
ReflectAtts.reflections = (1, 0, 0, 0, 1, 0, 0, 0)
ReflectAtts.planePoint = (0, 0, 0)
ReflectAtts.planeNormal = (0, 0, 0)
ReflectAtts.reflectType = ReflectAtts.Axis  # Plane, Axis
SetOperatorOptions(ReflectAtts, 0, 1)
SetTimeSliderState(0)
# Logging for SetAnnotationObjectOptions is not implemented yet.
# Logging for SetAnnotationObjectOptions is not implemented yet.
SetActivePlots(0)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -3.25
PseudocolorAtts.useBelowMinColor = 0
PseudocolorAtts.belowMinColor = (0, 0, 0, 255)
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 0
PseudocolorAtts.useAboveMaxColor = 0
PseudocolorAtts.aboveMaxColor = (0, 0, 0, 255)
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "bhdisk_opaque"
PseudocolorAtts.invertColorTable = 0
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
AddOperator("Isosurface", 1)
IsosurfaceAtts = IsosurfaceAttributes()
IsosurfaceAtts.contourNLevels = 35
IsosurfaceAtts.contourValue = (-3.2, -3.125, -3.05, -2.975, -2.9, -2.825, -2.75, -2.675, -2.6, -2.525, -2.45, -2.375, -2.3, -2.225, -2.15, -2.075, -2, -1.925, -1.85, -1.775, -1.7, -1.625, -1.55, -1.475, -1.4, -1.325, -1.25, -1.175, -1.1, -1.025, -0.95, -0.875, -0.8, -0.725, -0.65)
IsosurfaceAtts.contourPercent = (0.1)
IsosurfaceAtts.contourMethod = IsosurfaceAtts.Value  # Level, Value, Percent
IsosurfaceAtts.minFlag = 1
IsosurfaceAtts.min = -4
IsosurfaceAtts.maxFlag = 1
IsosurfaceAtts.max = 0
IsosurfaceAtts.scaling = IsosurfaceAtts.Linear  # Linear, Log
IsosurfaceAtts.variable = "logrho"
SetOperatorOptions(IsosurfaceAtts, 0, 1)
SetActivePlots(2)
VectorAtts = VectorAttributes()
VectorAtts.glyphLocation = VectorAtts.UniformInSpace  # AdaptsToMeshResolution, UniformInSpace
VectorAtts.useStride = 0
VectorAtts.stride = 1
VectorAtts.nVectors = 100000
VectorAtts.lineWidth = 3
VectorAtts.scale = 0.2
VectorAtts.scaleByMagnitude = 1
VectorAtts.autoScale = 0
VectorAtts.headSize = 0.3
VectorAtts.headOn = 1
VectorAtts.colorByMag = 0
VectorAtts.useLegend = 0
VectorAtts.vectorColor = (255, 255, 0, 255)
VectorAtts.colorTableName = "Default"
VectorAtts.invertColorTable = 0
VectorAtts.vectorOrigin = VectorAtts.Tail  # Head, Middle, Tail
VectorAtts.minFlag = 0
VectorAtts.maxFlag = 0
VectorAtts.limitsMode = VectorAtts.OriginalData  # OriginalData, CurrentPlot
VectorAtts.min = 0
VectorAtts.max = 1
VectorAtts.lineStem = VectorAtts.Line  # Cylinder, Line
VectorAtts.geometryQuality = VectorAtts.Fast  # Fast, High
VectorAtts.stemWidth = 0.08
VectorAtts.origOnly = 1
VectorAtts.glyphType = VectorAtts.Arrow  # Arrow, Ellipsoid
VectorAtts.animationStep = 0
SetPlotOptions(VectorAtts)
AddOperator("Box", 1)
SetActivePlots(2)
BoxAtts = BoxAttributes()
BoxAtts.amount = BoxAtts.Some  # Some, All
BoxAtts.minx = 0
BoxAtts.maxx = 1
BoxAtts.miny = 0
BoxAtts.maxy = 1
BoxAtts.minz = 0
BoxAtts.maxz = 1
BoxAtts.inverse = 0
SetOperatorOptions(BoxAtts, 0, 1)
SetActivePlots(2)
DrawPlots()
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.561063, -0.562408, 0.607376)
View3DAtts.focus = (0, 0, 0)
View3DAtts.viewUp = (0.514173, 0.338247, 0.788172)
View3DAtts.viewAngle = 22.8952
View3DAtts.parallelScale = 50.625
View3DAtts.nearPlane = -500
View3DAtts.farPlane = 500
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (0, 0, 0)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 0
SetView3D(View3DAtts)
# End spontaneous state

View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.561063, -0.562408, 0.607376)
View3DAtts.focus = (0, 0, 0)
View3DAtts.viewUp = (0.514173, 0.338247, 0.788172)
View3DAtts.viewAngle = 22.8952
View3DAtts.parallelScale = 50.625
View3DAtts.nearPlane = -500
View3DAtts.farPlane = 500
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (0, 0, 0)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 0
SetView3D(View3DAtts)
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 1
SaveWindowAtts.outputDirectory = "."
SaveWindowAtts.fileName = "/anvil/scratch/x-yguo11/bhdisk_sol_05/_opacity_probe/D_c018_d35_"
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY, EXR
SaveWindowAtts.width = 1920
SaveWindowAtts.height = 1080
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.saveTiled = 0
SaveWindowAtts.quality = 80
SaveWindowAtts.progressive = 0
SaveWindowAtts.binary = 0
SaveWindowAtts.stereo = 0
SaveWindowAtts.compression = SaveWindowAtts.None  # None, PackBits, Jpeg, Deflate, LZW
SaveWindowAtts.forceMerge = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint  # NoConstraint, EqualWidthHeight, ScreenProportions
SaveWindowAtts.pixelData = 2
SaveWindowAtts.advancedMultiWindowSave = 0
SaveWindowAtts.subWindowAtts.win1.position = (0, 0)
SaveWindowAtts.subWindowAtts.win1.size = (128, 128)
SaveWindowAtts.subWindowAtts.win1.layer = 0
SaveWindowAtts.subWindowAtts.win1.transparency = 0
SaveWindowAtts.subWindowAtts.win1.omitWindow = 0
SaveWindowAtts.subWindowAtts.win2.position = (0, 0)
SaveWindowAtts.subWindowAtts.win2.size = (128, 128)
SaveWindowAtts.subWindowAtts.win2.layer = 0
SaveWindowAtts.subWindowAtts.win2.transparency = 0
SaveWindowAtts.subWindowAtts.win2.omitWindow = 0
SaveWindowAtts.subWindowAtts.win3.position = (0, 0)
SaveWindowAtts.subWindowAtts.win3.size = (128, 128)
SaveWindowAtts.subWindowAtts.win3.layer = 0
SaveWindowAtts.subWindowAtts.win3.transparency = 0
SaveWindowAtts.subWindowAtts.win3.omitWindow = 0
SaveWindowAtts.subWindowAtts.win4.position = (0, 0)
SaveWindowAtts.subWindowAtts.win4.size = (128, 128)
SaveWindowAtts.subWindowAtts.win4.layer = 0
SaveWindowAtts.subWindowAtts.win4.transparency = 0
SaveWindowAtts.subWindowAtts.win4.omitWindow = 0
SaveWindowAtts.subWindowAtts.win5.position = (0, 0)
SaveWindowAtts.subWindowAtts.win5.size = (128, 128)
SaveWindowAtts.subWindowAtts.win5.layer = 0
SaveWindowAtts.subWindowAtts.win5.transparency = 0
SaveWindowAtts.subWindowAtts.win5.omitWindow = 0
SaveWindowAtts.subWindowAtts.win6.position = (0, 0)
SaveWindowAtts.subWindowAtts.win6.size = (128, 128)
SaveWindowAtts.subWindowAtts.win6.layer = 0
SaveWindowAtts.subWindowAtts.win6.transparency = 0
SaveWindowAtts.subWindowAtts.win6.omitWindow = 0
SaveWindowAtts.subWindowAtts.win7.position = (0, 0)
SaveWindowAtts.subWindowAtts.win7.size = (128, 128)
SaveWindowAtts.subWindowAtts.win7.layer = 0
SaveWindowAtts.subWindowAtts.win7.transparency = 0
SaveWindowAtts.subWindowAtts.win7.omitWindow = 0
SaveWindowAtts.subWindowAtts.win8.position = (0, 0)
SaveWindowAtts.subWindowAtts.win8.size = (128, 128)
SaveWindowAtts.subWindowAtts.win8.layer = 0
SaveWindowAtts.subWindowAtts.win8.transparency = 0
SaveWindowAtts.subWindowAtts.win8.omitWindow = 0
SaveWindowAtts.subWindowAtts.win9.position = (0, 0)
SaveWindowAtts.subWindowAtts.win9.size = (128, 128)
SaveWindowAtts.subWindowAtts.win9.layer = 0
SaveWindowAtts.subWindowAtts.win9.transparency = 0
SaveWindowAtts.subWindowAtts.win9.omitWindow = 0
SaveWindowAtts.subWindowAtts.win10.position = (0, 0)
SaveWindowAtts.subWindowAtts.win10.size = (128, 128)
SaveWindowAtts.subWindowAtts.win10.layer = 0
SaveWindowAtts.subWindowAtts.win10.transparency = 0
SaveWindowAtts.subWindowAtts.win10.omitWindow = 0
SaveWindowAtts.subWindowAtts.win11.position = (0, 0)
SaveWindowAtts.subWindowAtts.win11.size = (128, 128)
SaveWindowAtts.subWindowAtts.win11.layer = 0
SaveWindowAtts.subWindowAtts.win11.transparency = 0
SaveWindowAtts.subWindowAtts.win11.omitWindow = 0
SaveWindowAtts.subWindowAtts.win12.position = (0, 0)
SaveWindowAtts.subWindowAtts.win12.size = (128, 128)
SaveWindowAtts.subWindowAtts.win12.layer = 0
SaveWindowAtts.subWindowAtts.win12.transparency = 0
SaveWindowAtts.subWindowAtts.win12.omitWindow = 0
SaveWindowAtts.subWindowAtts.win13.position = (0, 0)
SaveWindowAtts.subWindowAtts.win13.size = (128, 128)
SaveWindowAtts.subWindowAtts.win13.layer = 0
SaveWindowAtts.subWindowAtts.win13.transparency = 0
SaveWindowAtts.subWindowAtts.win13.omitWindow = 0
SaveWindowAtts.subWindowAtts.win14.position = (0, 0)
SaveWindowAtts.subWindowAtts.win14.size = (128, 128)
SaveWindowAtts.subWindowAtts.win14.layer = 0
SaveWindowAtts.subWindowAtts.win14.transparency = 0
SaveWindowAtts.subWindowAtts.win14.omitWindow = 0
SaveWindowAtts.subWindowAtts.win15.position = (0, 0)
SaveWindowAtts.subWindowAtts.win15.size = (128, 128)
SaveWindowAtts.subWindowAtts.win15.layer = 0
SaveWindowAtts.subWindowAtts.win15.transparency = 0
SaveWindowAtts.subWindowAtts.win15.omitWindow = 0
SaveWindowAtts.subWindowAtts.win16.position = (0, 0)
SaveWindowAtts.subWindowAtts.win16.size = (128, 128)
SaveWindowAtts.subWindowAtts.win16.layer = 0
SaveWindowAtts.subWindowAtts.win16.transparency = 0
SaveWindowAtts.subWindowAtts.win16.omitWindow = 0
SaveWindowAtts.opts.types = ()
SaveWindowAtts.opts.help = ""
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()
