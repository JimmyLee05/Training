#import <SceneKit/SceneKit.h>

#define WALL_WIDTH 		0.02
#define WALL_HEIGHT 	2.5
#define WALL_LENGHT 	2.5

#define DOOR_WIDTH 		0.5
#define DOOR_HEIGHT 	1.5

@interface transDimentStruct: SCNNode
+ (SCNNode *) planeWithMaskUpperSide: (BOOL)isMaskUpper;
+ (SCNNode *) wallSegmentNodeWithLenght: (CGFloat)length height:(CGFloat)height maskRightSide: (BOOL) isMaskRightSide;
+ (SCNNode *) doorFrame;
+ (SCNNode *) innnerStructs;
+ (BOOL) checkIfUserInRoom;

@end