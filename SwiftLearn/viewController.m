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

	
}