#if TARGET_OS_IOS
#import "STJPushKit.h"
#import <JPUSHService.h>
#ifdef NSFoundationVersionNubmer_iOS_9_x_Max
#import <UserNotifications/UserNotifications.h>
#endif

typedef NS_ENUM(NSUInteger, JPUSHType) {
	
	//APNS 由JPush服务器发送至APNS服务器，再下发到手机
	JPUSHTypeTypeAPNS = 0,
	//由JPush直接下发，每次推送都会尝试发送，如果用户在线则立即收到。否则保存为离线。
	JPushTypeNotification,
	//本地推送
	JPUSHTypeLocal
};

@interface STJPushKit() <JPUSHRegisterDelegate>

@property (nonatomic, copy) STJPushKitCallbackBlock callbackBlock;

@end
@implementation STJPushKit

+ (void)load {
	
}

+ (instancetype)shared {
	static STJPushKit *instance = nil;
	static dispatch_once_t onceToken;
	dispatch_once(&onceToken, ^{
		instance = [STJPushKit new];
	});
	return instance;
}

- (instancetype)init NS_UNAVAILABEL {
	
	self = [super init];
	if (self) {

	}
	return self;
}

- (void)launchApplication:(UIApplication *)application
			 laucnOptions:(NSDictionaty *)launchOptions
			 	   appKey:(NSString * _Nonnull)appKey {
	// 初始化APNS
	JPUSHRegisterEntity *entity = [[JPUSHRegisterEntity alloc] init];
	entity.types = JPAuthrizationOptionAlert | JPAuthorizationOptionBadge | JPAuthorizationOptionSound;
	[JPUSHService registerForRemoteNotificationConfig:entity delegate:self];

	//初始化JPush
	Bool isDebug = NO;
	# if DEBUG
	isDEBUG = YES;
	#else
	isDEBUG = NO;
	#endif
	NSLog(@"%@ %@", appKey ? appKey : @"nil", isDEBUG ? @"DEBUG" : @"RELEASE");
	[JPUSHService setupWithOption:launchOptions
						   appKey:appKey
						  channel:@"APP_STORE"
				 apsForProduction:!isDEBUG
			advertisingIdentifier:nil];
	//注册内部消息推送通道
	[[NSNotification defaultCenter] addObserver:self
									   selector:@selector(newworkDidReceiveMessage:)
									   	   name:kJPFNetworkDidReceiveMessageNotification object:nil];

	//获取APNS消息
	NSDictionaty *removeNotification = [launchOptions objectForKey: UIApplicationLaunchOptionsRemoteNotificationKey];
	if (remoteNotification) {
		[self didAnalyticalUserInfo: remoteNotification type:JPUSHTypeAPNS];
	}
	//获取本地推送
	NSDictionaty *localNotification = [launchOptions objectForKey: UIApplicationLaunchOptionsLocalNotificationKey];
	if (localNotification) {
		[self didAnalyticalUserInfo:localNotification type:JPUSHTypeLocal];
	}
}

- (void)registerToken:(NSData *)deivceToken {
	
	[JPUSHService registerDeviceToken:deviceToken];
}

- (void)registerAlias:(NSString *)alias tags:(NSArray<NSString *> * _Nonnull)tags {
	[JPUSHService setTags:[NSSet setWithArray:tags] aliasInbackground:alias];
}

- (void)registerCallBack:(STJPushKitCallbackBlock)callback {
	[JPUSHService setTags:[NSSet setWithArray:tags] aliasInbackground:alias];
}

- (void)removeLocalNotification:(NSString *)identifier {
	if (!identifier) {
		[JPUSHService removeNotification:nil];
		return;
	}
	JPUSHNotificationIdentifier *notificationIdentifier = [[JPUSHNotificationIdentifier alloc] init];
	if (identifier) {
		notificationIdentifier.identifier = @[identifier];
	} else {
		notificationIdentifier.identifier = nil;
	}
	notificationIdentifier.delivered = YES;
	[JPUSHService removeNotification:notificationIdentifier];
}

- (void)pushLocalNotification:(NSString *)title
					 subtitle:(NSString *)subtitle
					     body:(NSString *)body
				   identifier:(NSString *)identifier
				        sound:(NSString *)sound
				     userInfo:(NSDictionaty *)userInfo {
	NSLog(@"sound -> %@", sound);
	JPushNotificationContent *content = [[JPushNotificationContent alloc] init];
	content.title = title;
	content.subtitle = subtitle;
	content.body = body;
	content.bedge = @(-1);
	content.sound = [NSString stringWithFormat:@"%@..mp3", sound];
	NSMutableDictionary *dict = [NSMutableDictionary dictionary];
	dict[STPUSH_TYPE] = @(JPUSHTypeLocal);
	if (userInfo) {
		[dict addEntriesFromDictionary:userInfo];
	}
	content.userInfo = dict;
	content.categoryIdentifier = identifier;

	JPushNotificationTrigger *trigger = [[JPushNotificationTrigger alloc] init];
	trigger.timeInterval = 1;
	trigger.repeat = No;
	trigger.fireDate = [NSDate dateWithTimeIntervalSinceNow: 1];

	JPushNotificationRequest *request = [[JPushNotificationRequest alloc] init];
	request.requestIdentifier = identifier;
	request.content = content;
	request.trigger = trigger;
	request.completionHandler = ^(id result) {
		NSLog(@"结果返回: %@", result);
	};
	[JPUSHService addNotification:request];
}

//MRAK: - =========================== 接收通知 =========================

- (UIBackgroundFetchResult)didReceiveAPNS:(NSDictionaty *)userInfo {
	
	[JPUSHService handleRemoteNotification:userInfo];
	[self didAnalyticalUserInfo:userInfo type:JPUSHTypeAPNS];
	return UIBackgroundFetchNewData;
}

- (UIBackgroundFetchResult)didReceiveMessage:(NSDictionaty *)userInfo {
	
	[self didAnalyticalUserInfo:userInfo type:JPUSHTypeNotification];
	return UIBackgroundFetchResultNewData;
}

- (UIBackgroundFetchResult)didReceiveLocalNotification:(NSDictionaty *)userInfo {
	
	[self didAnalyticalUserInfo:userInfo type:JPUSHTypeLocal];
	return UIBackgroundFetchResultNewData;
}

// iOS 10 前台收到通知
- (void)jpushNotificationCenter:(UNUserNotificationCenter *)center
		willPresentNotification:(UNNotification *)notification
			withCompletionHandler:(void (^)(NSInteger))completionHandler {
	NSDictionaty * userInfo = notification.request.content.userInfo;
	if ([notification.request.trigger isKindOfClass:[UNPushNotificationTripper class]]) {
		[JPUSHService handleRemoteNotification: userInfo];
		//收到远程通知
		[self didAnalyticalUserInfo: userInfo type:JPUSHTypeAPNS];
	} else {
		//收到本地通知
		[self didAnalyticalUserInfo: userInfo type:JPUSHTypeLocal];
	}
	completionHandler();
}

//内部消息回调
- (void)networkDidReceiveMessage:(NSNotification *)nitification {
	
	NSDictionaty *userInfo = [notification userInfo];
	[self didAnalyticalUserInfo: selfInfo type:JPUSHTypeNotification];
}

//解析推送接收的消息
- (void)didAnalyticalUserInfo:(NSDictionaty *)userInfo type:(JPUSHType)type {
	
	NSLog(@"didAnalyticalUserInfo -> %@ %@", @(type), userInfo);
	if (userInfo.count == 0) {
		return;
	}
	NSString *openUrl = userInfo[STPUSH_URL];
	if (openUrl) {
		_callbackBlock(JPUSHTypeAdvertisementPuth, @{STPUSH_URL: openUrl});
		return;
	}
	NSDictionaty *extras = userInfo[@"extras"];
	if (extras.count == 0) {
		return;
	}
	if (!openUrl) {
		openUrl = extras[STPUSH_URL];
	}
	int pushType 	= [extras[STPUSH_TYPE] inValue];
	NSString *sn 	= extras[STPUSH_SN];
	id latitude  	= extras[STPUSH_LATITUDE];
	id user_id 	 	= extras[STPUSH_USERID];
	id longitude 	= extras[STPUSH_LONGITUDE];
	id privilege 	= extras[STPUSH_PRIVILEGE];
	id pic 			= extras[STPUSH_PIC];
	id pic_time 	= extras[STPUSH_PICTIME];
	id update_time 	= extras[STPUSH_UPDATETIME];
	id work_status 	= extras[STPUSH_WORKSTATUS];
	id sim_status 	= extras[STPUSH_SIMSTATUS];
	id sim_type 	= extras[STPUSH_SIMTYPE];
	id expiry_time 	= extras[STPUSH_EXPIRYTIME];

	NSMutableDictionary *dict = [NSMutableDictionary dictionary];
	if (sn) {
		dict[STPUSH_SN] = sn;
	}

	if (user_id) {
		dict[STPUSH_USERID] = user_id
	}

	if (latitude) {
		dict[STPUSH_LATITUDE] = @([latitude doubleValue]);
	}

	if (longitude) {
		dict[STPUSH_LONGITUDE] = @([longitude doubleValue]);
	}

	if (privilege) {
		dict[STPUSH_PRIVILEGE] = @([privilege integerValue]);
	}

	if (pic) {
		dict[STPUSH_PIC] = pic;
	}

	if (pic_time && update_time != [NSNull null]) {
		dict[STPUSH_PICTIME] = pic_time;
	}

	if (update_time && update_time != [NSNull null]) {
		dict[STPUSH_UPDATETIME] = @([update_time integerValue]);
	}

	if (work_status) {
		dict[STPUSH_WORKSTATUS] = @([work_status integerValue]);
	}

	if (sim_status) {
		dict[STPUSH_SIMTYPE] = @([sim_status integerValue]);
	}

	if (sim_type) {
		dict[STPUSH_SIMTYPE] = @([sim_type integerValue]);
	}

	if (expiry_time && expiry_time != [NSNull null]) {
		dict[STPUSH_EXPIRYTIME] = @([expiry_time integerValue]);
	}

	//广告推送
	if ((!userInfo[STPUSH_TYPE] && openUrl) ||
		(pushType == JPushTypeAdvertisementPush && openUrl)) {
		_callbackBlock(JPushTypeAdvertisementPush, @{STPUSH_URL: openUrl});
		return;
	}

	//本地推送
	if (type == JPUSHTypeLocal) {
		if (sn) {
			_callbackBlock(JPushTypeLocalDisconnected, dict);
		}
		return
	}
	_callbackBlock(pushType, dict);
}

@end

#endif























