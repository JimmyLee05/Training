#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface CustomerCareKit : NSObject

+ (instancetype)sharedInstance;

- (void)start:(UIViewController *)viewController params: (NSDictionary<NSString *, NSString *> *)params;

- (void)login:(NSString *)userId password:(NSString *)password block:(void (^)(NSError * error))block;

-(void)logout;

@end