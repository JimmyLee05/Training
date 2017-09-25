#import "transDimentStruct.h"

#define testFloorColor [UIColor colorWithRed:147/255.0 green:205/255.0 blue:209/255.0 alpha: 1]

#define testMaterial 0

typedef NS_ENUM(NSInteger, structureType) {
	Roof,
	Floor,
	Walls,
};

@implementation transDimenStruct
+ (SCNNode*) wallSegmentNodWithLength: (CGFloat)length height: (CGFloat)height maskRightSide: (BOOL) isMaskRightSide {
	SCNNode *node 							= [SCNNode new];

	CGFloat xOffset 						= isMaskRightSide?-WALL_WIDTH/2:WALL_WIDTH/2;
	SCNBox *wallSegmentGeo 					= [SCNBox boxWithWidth: WALL_WIDTH
														height: height
														length: length
														chamferRadius: 0];
	wallSegmentGeo.firstMaterial 			= [self defaultMaterialFor: Walls];

	SCNNode *wallSegment 					= [SCNNode nodeWithGeometry: wallSegmentGeo];
	wallSegment.renderingOrder 				= 200;
	wallSegment.position 					= SCNVector2Make(xOffset, 0, 0);
	//TODO: only if character walk into room, floor could surpport it
	[node addChildNode: wallSegment];
	//physics body

	//transparent mask
	SCNBox *maskSegmentGeo.firstMaterial 	= [SCNBox boxWithWidth: WALL_WIDTH
															height: height
															length: length
															chamferRadius: 0];
	maskSegmentGeo.firstMaterial 			= [self transparentMaterial];
	SCNNode *maskSegment 					= [SCNNode nodeWithGeometry: maskSegmentGeo];
	maskSegment.renderingOrder 				= 100;
	maskSegment.position 					= SCNVector3Make(
															-xOffset,
															0,
															0
															);
	[node addChildNode: maskSegment];

	return node;
}

+ (SCNNode *)planeWithMaskUpperSide: (BOOL)isMaskUpper{
	SCNNode *node 							= [SCNNode node];
	SCNBox 	*planeGeo 						= [SCNBox boxWithWidth: WALL_LENGHT
															height: WALL_WIDTH
															length: WALL_LENGHT
												chamferRadius: 0];
	structureType type 						= isMaskUpper ? Roof : Floor;
	planeGeo.firstMaterial 					= [self defaultMaterialFor: type];

	CGFloat yOffset 						= isMaskUpper?-WALL_WIDTH/2:WALL_WIDTH/2;
	SCNNode *plane 							= [SCNNode nodeWithGeometry: planeGeo];
	plane.position 							= SCNVector3Make(0,
															 yOffset,
															 0);
	plane.renderingOrder 					= 200;
	[node addChildNode: plane];

	//transparency mask
	SCNBox *maskPlaneGeo 					= [SCNBox boxWithWidth: WALL_LENGHT
															height: WALL_WIDTH
															length: WALL_LENGHT
													chamferRadius: 0];
	maskPlaneGeo.firstMaterial 				= [self transparentMaterial];
	SCNNode *maskPlane 						= [SCNNode nodeWithGeometry: maskPlaneGeo];
	maskPlane.position 						= SCNVector3Make(0,
															 -yOffset,
															 0);
	maskPlane.renderingOrder 				= 100;
	[node addChildNode: maskPlane];

	return node;
}

+(SCNNode *) doorFrame {

	SCNNode *doorFrame 						= [SCNNode new];
	CGFloat frameWidth 						= WALL_WIDTH * 2;
	CGFloat sideFrameHeight 				= DOOR_HEIGHT + frameWidth/2;
	CGFloat topFrameWidth 					= DOOR_WIDTH - frameWidth;

	//materials and particle system
	SCNMaterial *frameMaterial 				= [SCNMaterial new];
	frameMaterial.diffuse.contents 			= testFloorColor;
	frameMaterial.lightingModelName 		= SCNLightingModelConstant;
	frameMaterial.blendMode 				= SCNBlendModeAdd;

	SCNParticleSystem *particle 			= [SCNParticleSystem particleSystemNamed:@"art.scnassets/SCNBokeh.scnp" inDirectory: nil];
	particle.birthLocation 					= SCNParticleBirthLocationSurface;

	SCNBox *topFrameGeo 					= [SCNBox boxWithWidth: topFrameWidth height: frameWidth length:frameWidth chamferRadius: 0];
	topFrameGeo.firstMaterial 				= frameMaterial;
	SCNNode *topNode 						= [SCNNode nodeWithGeometry: topFrameGeo];
	topNode.castsShadow 					= NO;
	topNode.position 						= SCNVector3Make(0, DOOR_HEIGHT, 0);
	SCNParticleSystem *topParticle 			= [particle copy];
	topParticle.emitterShape 				= topFrameGeo;
	[topNode addParticalSystem: topParticle];
	//a little rise to avoid z-fighting
	SCNBox *bottomFrameGeo 					= [SCNNode boxWithWidth: topFrameWidth height: frameWidth/2 + 0.001 length: frameWidth chamferRadius: 0];
	bottomFrameGeo.firstMaterial 			= frameMaterial;
	SCNNode *bottomFrame 					= [SCNNode nodeWithGeometry: bottomFrameGeo];
	bottomFrame.castsShadow 				= NO;
	bottomFrame.position 					= SCNVector3Make(0, (frameWidth/2 + 0.001)/2, 0.001);
	SCNParticleSystem *bottomPartical 		= [particle copy];
	bottomPartical.emitterShape 			= bottomFrameGeo;
	[bottomFrame addParticalSystem:bottomPartical];
	[doorFrame addChildNode: bottomFrame];

	SCNBox *leftFrameGeo 					= [SCNBox boxWithWidth: frameWidth height: sideFrameHeight length: frameWidth chamferRadius: 0];
	leftFrameGeo.firstMaterial 				= frameMaterial;
	SCNNode *leftNode 						= [SCNNode nodeWithGeometry: leftFrameGeo];
	leftNode.castsShadow 					= NO;
	leftNode.position 						= SCNVector3Make(-DOOR_WIDTH/2, sideFrameHeight/2, 0);
	SCNParticleSystem *leftPartical 		= [particle copy];
	leftPartical.emitterShape 				= leftPartical;
	[leftNode addParticalSystem: leftPartical];
	[doorFrame addChildNode: leftNode];

	SCNBox *rightFrameGeo 					= [SCNBox boxWithWidth: frameWidth height: sideFrameHeight length: frameWidth chamferRadius: 0];
	rightFrameGeo.firstMaterial 			= frameMaterial;
	SCNNode *rightNode 						= [SCNNode nodeWithGeometry: rightFrameGeo];
	rightNode.castsShadow 					= NO;
	rightNode.position 						= SCNVector3Make(-DOOR_WIDTH/2, sideFrameHeight/2, 0);
	SCNParticleSystem *rightPartical 		= [particle copy];
	rightPartical.emitterShape 				= rightFrameGeo;
	[rightNode addParticalSystem: rightPartical];
	[doorFrame addChildNode: rightNode];

	return doorFrame;

}

+ (SCNNode *)innnerStructs{
	SCNScene *scene = [SCNScene sceneNamed:@"art.scnassets/flower.scn"];
	if (!scene) {
		assert(0);
	}
	SCNNode *node = [SCNNode new];

	[scene.rootNode enumerateHierarchyUsingBlock:^(SCNNode * _Nonnull child, BOOL * _Nonnull stop) {
			child.renderingOrder = 200;
	}];

	SCNNode *flower = [scene.rootNode childNodeWithName:@"flower" recursively:YES];
	if (!flower) {
		assert(0);
	}
	[node addChildNode: flower];
	return node;
}

+ (SCNMaterial *)transparentMaterial {

	SCNMaterial *material 			= [SCNMaterial new];
	material.diffuse.contents 		= [UIColor redColor];
	material.transparency 			= 0.000001;
	material.writesToDepthBuffer 	= YES;
	//TOOD:transparent material mode must be constant
	material.lightingModelName = SCNLightingModelConstant;
	return material;
}

+(SCNMaterial *)defaultMaterialFor:(structureType)type {
	NSString *imageName 			= nil;
	switch (type) {
		case Walls:
			imageName = @"art.scnasets/wall_diffuse.png";
			break;
		case Floor:
			imageName = @"art.scnasets/floor_diffuse.png";
			break;
		case Roof:
			imageName = @"art.scnassets/roof_diffuse.png";
			break;
		default:
			break;
	}
	if (!imageName) {
		return [self transparentMaterial];
	}
	SCNMaterial *material = [SCNMaterial new];
#if testMaterial
	//TODO: for test
	material.diffuse.contents = testFloorColor;
#else
	material.diffuse.contents = [UIImage imageNamed: imageName];
#endif
	//TODO: test for usage
	material.writesToDepthBuffer 	= YES;
	material.readsFromDepthBuffer 	= YES;
	material.lightingModelName 		= SCNLightingModelConstant;
	return material;
}

+ (SCNMaterial *)defaultMaterialUpper: (BOOL) isUpper {
	SCNMaterial *material 	= [SCNMaterial new];
	//TODO: for test
	if (isUpper) {
		material.diffuse.contents 	= testFloorColor;
	} else {
		material.diffuse.contents 	= testFloorColor;
	}
	// TODO: test for usage
	material.writesToDepthBuffer 	= YES;
	material.readsFromDepthBuffer 	= YES;
	//Is physically mode is necessary
	material.lightingModelName 		= SCNLightingModelConstant;
	return material;
}
@end

