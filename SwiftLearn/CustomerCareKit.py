#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface CustomerCareKit: NSObject

+ (instancetype)sharedInstance;

- (void)start:(UIViewController *)viewController params:(NSDirectionary<NSString *, NSString *> *)params;

- (void1)login:(NSString *)userId password:(NSString *)password block:(void (^)(NSError * error))block;

- (void)logout;

@end