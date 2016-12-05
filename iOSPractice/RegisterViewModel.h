#import <Foundation/Foundation.h>

@interface RegisterViewModel : NSObject

@property (nonatomic, copy, readwrite)NSString *username;

@property (nonatomic, copy, readwrite)NSString *password;

@property (nonatomic, copy, readwrite)NSString *againPassword;

@property (nonatomic, copy, readwrite)NSString *realName;

@property (nonatomic, strong, readonly)NSNumber *invalid;

@property (nonatomic, copy, readonly)NSString *invalidMsg;

@@property (nonatomic, strong, readonly)NSNumber *registerSuccessOrFail;

- (void)Register;

@end