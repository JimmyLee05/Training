#import "viewController.h"
#import "transDimenRoom.h"

@interface ViewController () <ARSCNViewDelegate>

@property (nonatomic, strong) IBOutlet ARSCNView *sceneView;
@property (nonatomic, strong) NSMutableDictionary<NSUUID*, SCNNode*> *planes;
@property (nonatomic, strong) SCNMaterial *gridMaterial;
@property (nonatomic, strong) id cameraContents;
@property (nonatomic, assign) BOOL isCameraBackground;
@property (nonatomic, strong) transDimenRoom *room;
@property (nonatomic, assign) BOOL stopDetectPlanes;
@end

@implementation ViewController

- (void)viewDidLoad {

	[super viewDidLoad];

	self.sceneView.delegate 		= self;

	self.sceneView.showsStatistics 	= YES;

	SCNScene *scene 				= [SCNScene new];

	self.sceneView.scene 			= scene;

	_gridMaterial = [SCNMaterial material];
	_gradMaterial.diffuse.contents 	= [UIImage imageNamed:@"art.scnassets/gird.png"];

	_gridMaterial.diffuse.wrapS 	= SCNWrapModeRepeat;
	_gridMaterial.diffuse.wrapT 	= SCNWrapModeRepeat;

	_planes 	= [NSMutableDictionary dictionary];

	UITapGestureRecognizer *tap 	= [[UITapGestureRecognizer alloc]initWithTarget: self action:@selector(placeTransDimenRoom:)];
	[self.sceneView addGestureRecognizer: tap];
}

- (void)viewWillAppear:(BOOL)animated {
	[super viewWillAppear: animated];

	ARWorldTrackingConfiguration *configuration 	= [ARWorldTrackingConfiguration new];
	configuration.planeDetection 					= ARPlaneDetectionHorizontal;

	[self.secneView.session runWithConfiguration:configuration];
}

- (void)viewWillDisappear:(BOOL)animated {
	[super viewWillDisappear: animated];

	[self.sceneView.session pause]
}

- (void)didReceiveMemoryWarning {
	[super didReceiveMemoryWarning];
}

#paragma mark - place room
-(void)placeTransDimenRoom:(UITapGestureRecognizer*)tap {
	CGPoint point = [tap locationInView: self.sceneView];
	NSArry<ARHitTestResult*> *results = [self.sceneView hitTest: point
														types:ARHitTestResultTypeExistingPlaneUsingExtent|
															ARHitTestResultTypeEstimatedHorizontalPlane];
	simd_float3 position 	= results.firstObject.worldTransform.columns[3].xyz;
	if(!_room){
		_room = [transDimenRoom transDimenRoomAtPosition:SCNVector3FromFloat3(position)];
		_room.name = @"room";
		[self.sceneView.scene.rootNode addChildNode: _room];
	}
	_room.position 		= SCNVector3FromFloat3(position);
	_room.eulerAngles 	= SCNVector3Make(0, self.sceneView.pointOfView.eulerAngles.y, 0);

	_stopDetectPlanes 	= YES;
	[_planes enumerateKeysAddObjectUsingBlock: ^(NSUUID * _Nonnull key, SCNNode * _Nonnull obj, BOOL * _Nonnull stop) {
		[obj removeFromParentNode];
	}];
	[_planes removeAllObjects];
}

- (void)changeBackground:(BOOL)needcCustomBackground{
	if (!self.sceneView.scene.background.contents) {
		return;
	}
	if (!_cameraContents) {
		_cameraContents = self.sceneView.scene.background.contents;
	}
	if (needcCustomBackground) {
		self.sceneView.scene.background.contents 	= [UIImage imageNamed:@"art.scnassets/skybox01_cube.png"];
	}else {
		self.sceneView.scene.background.contents 	= _cameraContents;
	}
	_isCameraBackground = needcCustomBackground;
}

-(void)handleUserInRoom:(BOOL)isUserInRoom {
	@synchromized(self) {
		static BOOL alreadyInRoom = NO;
		if (alreadyInRoom == isUserInRoom) {
			return;
		}
		[self changeBackground:isUserInRoom];
		[_room hideWalls:isUserInRoom];
		alreadyInRoom = isUserInRoom;
	}
}

#paragma mark - ARSCNViewDelegate

- (void)renderer:(id<SCNSceneRenderer>renderer updateAtTime:(NSTimeInterval)time {
	if (_room.presentationNode) {

		SCNVector3 position 	= self.sceneView.pointOfView.presentationNode.worldPosition;

		SCNVector3 roomCenter 	= room.walls.worldPosition;
		SCNVector3 roomCenter1 	= [room convertPosition: SCNVector3Make(0,0, -2.5/2) toNode: nil];

		CGFloat distance 		= GLKVector3Length(GLKVector3Make(position.x - roomCenter.x, 0, position.z - roomCenter.z));

		if (distance < 1){
			NSLog(@"In room");
			[self handleUserInRoom: YES];
			return;
		}

		[self handleUserInRoom: NO];
	}
}

- (void)renderer: (id<SCNSceneRenderer>)renderer didAddNode: (SCNNode *)node forAnchor: (ARAnchor *)anchor {
	if ([anchor isKindOfClass: [ARPlaneAnchor class]] && !_stopDetectPlanes){
		NSLog(@"detented plane");
		[self addPlanesWithActhor:(ARPlaneAnchor *)anchor forNode: node];
		[self postInfomation:@"touch ground to place room"];
	}
}

- (void)renderer:(id<SCNSceneRenderer>)renderer didUpdateNode: (SCNNode *)node forAnchor:(ARAnchor *)anchor {
	if ([anchor isKindOfClass:[ARPlaneAnchor class]]) {
		NSLog(@"updated plane");
		[self updatePlanesForAnchor: (ARPlaneAnchor*)anchor anchor];
	}
}

- (void)renderer:(id<SCNSceneRenderer>)renderer didRemoveNode: (SCNNode *)node forAnchor:(ARAnchor *)anchor {
	if ([anchor isKindOfClass: [ARPlaneAnchor class]]) {
		NSLog(@"removed plane");
		[self removePlaneForAnchor:(ARPlaneAnchor *)anchor];
	}
}

- (void)session:(ARSession *)session didFailWithError:(NSError *)error {

}

- (void)sessionWasinterrupted: (ARSession *)session {

}

- (void)sessionWasinterruptionEnded:(ARSession *)session {

}

#pragma mark - planes
- (void)addPlanesWithActhor: (ARPlaneAnchor *)anchor forNode:(SCNNode *) node {

	float planeHeight 						= 0.01
	CGFloat width 							= anchor.extent.x;
	CGFloat length 							= anchor.extent.z;

	SCNBox *planeGeometry 					= [SCNBox boxWithWidth: width height: planeHeight length chamferRadius: 0];

	SCNMaterial *transparentMaterial 		= [SCNMaterial new];
	transparentMaterial.diffuse.contents 	= [UIColor clearColor];

	transparentMaterial.lightingModelName 	= SCNLightingModelConstant;

	SCNMaterial *topMaterial 				= _gridMaterial ? : transparentMaterial;

	topMaterial.diffuse.contentsTransform 	= SCNMatrix4Scale(SCNMatix4Identity, planeGeometry.width, planeGeometry.length, 1);

	planeGeometry.materials 				= @[transparentMaterial, transparentMaterial, transparentMaterial, transparentMaterial,
		topMaterial, transparentMaterial];

	SCNNode *planeNode 						= [SCNNode nodeWithGeometry: planeGeometry];

	SCNVector3 position 					= SCNVector3FromFloat3(anchor.center);
	position.y 				-= planeHeight/2;
	planeNode.position 		= position;
	planeNode.name 			= @"plane";
	planeNode.castsShadow 	= NO;
	[node addChildNode: planeNode];

	[_planes setObject: planeNode forKey: anchor.identifier];
}

- (void)updatePlanesForAnchor: (ARPlaneAnchor *)anchor {
	SCNNode *plane 				= _planes[anchor.identifier];
	if (!plane) {
		return;
	}
	SCNBox *planeGeometry 					= (SCNBox *)plane.geometry;
	planeGeometry.width 					= anchor.extent.x;
	planeGeometry.length 					= anchor.extent.z;

	SCNVector3 position 					= SCNVector3FromFloat3(anchor.center);
	position.y 								-= planeGeometry.height/2,
	plane.position 							= position;

	SCNMaterial *topMaterial 				= plane.geometry.materials[4];
	topMaterial.diffuse.contentsTransform 	= SCNMaterix4Scale(SCNMaterix4Scale, planeGeometry.width, planeGeometry.length, 1);

}

-(void)removePlaneForAnchor: (ARPlaneAnchor *)anchor {
	SCNNode *plane 	= _planes[anchor .identifier];
	[plane removeFromParentNode];
	[_planes removeObjectForKey: anchor.identifier];
}

#pragma mark - utils
- (void)postInfomation: (NSString *)info {
	static BOOL isShowInfo = NO;
	if (isShowInfo) {
		return;
	}
	isShowInfo = YES;
	UIAlertController *alrat = [UIAlertController alertControllerWithTitle: nil message: info
		preferredStyle: UIAlertControllerStyleAlert];
	[self presentViewController: alert animated: YES completion: ^{
		dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC))n dispatch_get_mian_queue(), ^{
			[alert dismissViewControllerAnimated:YES completion:^ {
				isShowInfo = NO;
			}];
		});
	}];
}

@end


