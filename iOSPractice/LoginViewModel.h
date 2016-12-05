#import <Foundation/Foundation.h>

@interface LoginViewModel : NSObject

@property (nonatomic, copy, readwrite)NSString *username;

@property (nonatomic, copy, readwrite)NSString *password;

@property (nonatomic, strong, readonly)NSNumber *invalid;

@property (nonatomic, copy, readonly)NSString *invalidMsg;

@property (nonatomic, strong, readonly)NSNumber *netFail;

@property (nonatomic, strong, readonly)NSNumber *loginSuccessOrFail;

-(void)login;

@end