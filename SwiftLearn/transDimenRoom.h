#import <SceneKit/SceneKit.h>

@interface transDimenRoom: SCNNode

@property (nonatomic, strong) SCNNode  *walls;
@property (nonatomic, strong) SCNLight *light;

+(instancetype)transDimenRoomAtPosition:(SCNVector3)position;

-(BOOL)checkIfInRoom:(SCNVector3)position;
-(void)hideWalls:(BOOL)hidden;

@end