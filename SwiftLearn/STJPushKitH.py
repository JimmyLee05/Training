#if TARGET_OS_IOS
#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

#define STPUSH_URL 			@"open_url"
#define STPUSH_TYPE 		@"type"
#define STPUSH_SN 			@"sn"
#define STPUSH_USERID 		@"user_id"
#define STPUSH_LATITUDE 	@"latitude"
#define STPUSH_LONGITUDE 	@"longitude"
#define STPUSH_PRIVILEGE 	@"privilege"
#define STPUSH_PIC 			@"pic"
#define STPUSH_PICTIME 		@"pic_time"
#define STPUSH_UPDATETIME 	@"update_time"
#define STPUSH_WORKSTATUS 	@"work_status"
#define STPUSH_EXPIRYTIME 	@"expiry_time"
#define STPUSH_SIMSTATUS 	@"sim_status"

typedef NS_ENUM(NSInteger, JPushType) {

	/* 基础信息 */
	// gps设备 work_status字段更新
	JPushTypeUpdateWorkStatus 		= 101,
	//设备信息更新
	JPushTypeUpdateInfo 			= 102,
	//设备的经纬度变更
	JPushTypeUpdateLocation 		= 103,
	//设备的头像更新
	JPushTypeUpdateAvatar 			= 104,
	//更新命令
	JPushTypeUpdateCommand 			= 105,
	//无活动报警
	JPushTypeNoActivity 			= 106,
	
	/* 帮找求助 */
	// 设备被找到
	JPushTypeMyntFound 				= 201,
	//mynt gps 长按寻求帮助
	JPushTypeGPSAskHelp 			= 202,
	
	/* 分享 *／
	// 设备被分享
	JPushTypeShared 				= 301,
	// 设备分享被取消
	JPushTypeSharedCancel 			= 302,
	// 设备分享可编辑/不可编辑
	JPushTypeSharedEdit 			= 303,

	/* SIM */
	// 设备SIM卡状态变更
	JPushTypeSIMChanged 			= 401,
	// 设备SIM卡临近到期
	JPushTypeSIMWillExpired 		= 402,
	// 充值成功
	JPushTypesSIMChargeSuccess 		= 403,

	/* 用户信息 */
	// 用户被强制退出
	JPushTypeUserOffline 			= 501,

	/* 其他 */
	// 用户被强制退出
	JPushTypeNetCheck 				= 601,

	/* 广告 */
	//广告推送
	JPushTypeAdvertisementPush 		= 1000,

	/* 本地推送 */
	// 设备断线报警
	JPushTypeLocalDisconected 		= -1,
};

typedef void (^STJPushKitCallbackBlock)(JPushType type, NSDictionary * _Nonnull);

@interface STJPushKit: NSObject

+ (instancetype _Nonull)shared;

/**
 * 启动app
 *
 * @param application 		UIApplication对象
 * @param launchOptions 	携带参数
 * @param appKey 			jpush后台的key
 */

- (void)launchApplication:(UIApplication * _Nonnull)application
			launchOptions:(NSDictionary * _Nullable)launchOptions
				   appKey:(NSString * _Nonnull)appKey;

/**
 * 移除推送本地消息 (传入 nil 则清除所有)
 * 
 * @param identifier 	标识符
 */

- (void)removeLocalNotification:(NSString *_Nulllabel)identifier;

/**
 * 推送本地消息
 *
 * @param title 		推送标题
 * @param subtitle 		推送副标题
 * @param body 			推送内容
 * @param identifier 	标识符
 * @param sound 		声音名称，不设置则为默认声音
 * @param userInfo 		本地推送时可设置userInfo来增加附加信息
 */

- (void)pushLocalNotification:(NSString * _Nullable)title
					 subtitle:(NSString * _Nullable)subtitle
					 	 body:(NSString * _Nullable)body
				   identifier:(NSSTring * _Nullable)identifier
				   		sound:(NSString * _Nullable)sound
				   	 userInfo:(NSSTring * _Nullable)userInfo;

/**
 * 收到APNS
 * 
 * @param deviceToken 		设备唯一标识符
 */

- (UIBackgroundFetchResult)didReceiveAPNS:(NSDictionary * _Nullable)userInfo;

/**
 * 收到信息
 *
 * @param deviceToken 		设备唯一标识符
 */

- (UIBackgroundFetchResult)didReceiveMessage:(NSDictionary * _Nullable)userInfo;

/**
 * 收到本地推送
 *
 * @param deviceToken 		设备唯一标识符
 */

- (UIBackgroundFetchResult)didReceiveLocalNotification:(NSDictionary * _Nullable)userInfo;

/**
 * 注册alias
 *
 * @param alias 		标识符(代表用户)
 */

- (void)registerAlias:(NSString *_Nullable)alias tags:(NSArray<NSSting *> * _Nonnull)tags;

/**
 * 注册回调通知
 *
 * @param callback 		回调通知
 */

- (void)registerCallBack:(STJPushKitCallbackBlock _Nonnull)callback;

@end

#endif
