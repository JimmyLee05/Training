#import "STMyntBluetooth.h"

@interface STMynt (SlightechPrivate)

//绑定密码
- (void)sendPassword:(NSString * _Nullable)password
			handler:(void (^ _Nullable)(NSError * _Nullable error))handler;

//校验密码
- (void)checkPassword:(NSString * _Nullable)password
			handler:(void (^ _Nullable)(NSError * _Nullable error))handler;

//写入运动灵敏度
- (void)writeMotionSensibility:(NSInterger)sensibility
			handler:(void (^ _Nullable)(NSError * _Nullable error))handler;

//写入运动灵敏度
- (void)writeDBM:(NSInterger)dbm
		handler:(void (^ _Nullable)(NSError * _Nullable error))handler;

@end

@interface STMyntBluetooth (SlightechPrivate)

//设置请求基础参数
+ (void)setPostBaseParams:(NSDictionary * _Nullable)params;

+ (void)setNetMode:(BOOL)isOffline;

@end