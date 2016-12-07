#import <Foundation/Foundation.h>

@class UserModel;

@interface UserStatusManager : NSObject

@property(nonatomic, strong, readwrite)NSNumber *enableVoice;

@property(nonatomic, strong, readwrite)NSNumber *enableRange;

@property(nonatomic, strong, readwrite)NSNumber *isLogin;

@property(nonatomic, strong, readwrite)NSNumber *haveChangeInfo;

@property(nonatomic, strong, readwrite)NSNumber *userModel;

+(UserStatusManager*)shareManager;

@end