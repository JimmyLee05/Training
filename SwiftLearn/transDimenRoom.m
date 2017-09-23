#import "transDimenRoom.h"
#import "transDimenStruct.h"
#import <GLKit/GLKit.h>

#define DTG(x) GLKMathDegreesToRadius((x))
@implementation transDimenRoom

CGFloat sideLength 			= WALL_LENGTH;
CGFloat halfSideLength  	= WALL_LENGTH * 0.5;
CGFloat halfWallHeight 		= WALL_HEIGHT * 0.5;
CGFloat yFix 				= WALL_WIDTH;

+(instancetype)transDimenRoomAtPosition:(SCNVector3)position{

	transDimenRoom *wrapperNode = [transDimenRoom new];

	SCNNode *walls 			= [SCNNode new];
	walls.name 				= @"walls";

	SCNNode *backWall 		= [transDimenStruct wallSegmentNodWithLength: sideLength height: WALL_HEIGHT maskRightSide: YES];
	backWall.eulerAngles 	= SCNVector3Make(0, DTG(90), 0);
	// TODO: change 1.5wall_length to a variable
	backWall.position 		= SCNVector3Make(0, halfWallHeight - yFix, -halfSideLength);
	backWall.name 			= @"backWall";
	backWall.castsShadow 	= NO;
	[walls addChildNode: backWall];

	SCNNode *leftWall 		= [transDimenStruct wallSegmentNodWithLength: sideLength height: WALL_HEIGHT maskRightSide: YES];
	leftWall.eulerAngles 	= SCNVector3Make(0, DTG(-180), 0);
	leftWall.position 		= SCNVector3Make(-halfSideLength, halfWallHeight - yFix, 0);
	leftWall.name 			= @"leftWall";
	leftWall.castsShadow 	= NO;
	[walls addChildNode: leftWall];

	SCNNode 
	
}



















