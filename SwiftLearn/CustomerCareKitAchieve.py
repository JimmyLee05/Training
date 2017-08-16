#import "CustomerCareKit.h"
#import "IMNoDataView.h"
#import <YWExtensionForCustomerServiceFMWK/YWExtensionForCustomerServiceFMWK.h>
#import <WXOpenIMSDKFMWK/YWFMWK.h>
#impoer <WXOutModule/YWUIFMWK.h>
#import "InputViewPluginImagePicker.h"

#define BaiChuanKey 	@"23728071"
#define CustomerName 	@"myntcrm"
#define ChinaGroupId 	@"161874886"
#define OtherGroupId 	@"161874882"

typedef enum : NSUInteger {
	
	SDKInitStateNone,
	SDKInitStateIniting,
	SDKInitStateSuccess,
} SDKInitState;

@implementation UINavigationController (Dismiss)

- (void)dismissViewController {
	[[CustomerCareKit sharedInstance] logout];
	[self dismissViewControllerAnimated: YES completion:nil];
}

@end

@interface CustomerCareKit() {
	SDKInitState _initState;
}

@property (strong, nonatomic, readwrite) YWIMKit * ywIMKit;

@end

@implementation CustomerCareKit

+ (instancetype)sharedInstance {
	static dispatch_once_t once;
	static CustomerCareKit *customerCoreKit;
	dispatch_once(&once, ^{
		customerCareKit = [[self alloc] init];
	});
	return customerCareKit;
}

- (instancetype)init {
	self = [super init];
	if (self) {
		[self initSDK];
	}
	return self;
}

- (void)initSDK {
	
	//设置环境
	[[YWAPI sharedInstance] setEnviroment: YWEnviromentRelease];
	[[YWAPI sharedInstance] getGlobalLogService].enableXcodeConsole = NO;
	//开启日志
	// [[YWAPI sharedInstance] setLogEnabled:YES];

	NSLog(@"SDKVersion:%@", [YWAPI sharedInstance].YWSDKIdentifier);

	NSError *error = nil;

	//异步初始化IM SDK
	__weak typeof(self) weakSelf = self;
	_initState = SDKInitStateIniting;
	[[YWAPI sharedInstance] asyncInitWithOwnAppKey:BaiChuanKey completionBlock:^(NSError *aError, NSDictionary *aResult) {
		if (error.code != 0 && error.code != YWSdkInitErrorCodeAlreadyInited) {
			//初始化失败 
		} else {
			if (error.code == 0) {
				//首次初始化成功
				//获取一个IMKit并持有
				weakSelf.ywIMKit = [[YWAPI sharedInstance] fetchIMKitForOpenIM];
				[weakSelf loadResource];
				[weakSelf loadAvatar];
				_initState = SDKInitStateSuccess; 
			} else {
				//已经初始化
			}
		}
	}];
}

- (void)loadAvatar {
	
	//设置客服的头像
	[self.ywIMKit setFetchProfileForEServiceBlock:^(YWPersion *aPerson, YWProfileProgressBlock aProgressBlock,
		YWPrifileCompletionBlock aCompletionBlock) {
		YWProfile *item = [[YWProfile alloc] init];
		item.person = aPerson;
		item.displayName = NSLocalizedString(@"Q_A", @"");
		item.avatar = [UIImage imageNamed:@"q_a_servant_icon"];
		aCompletionBlock(YES, item);
	}];
}

- (void)loadResource {
	NSString *bundleName = @"CustomerCareResource.bundle";
	NSString *bundlePath = [[NSBundle mainBundle].resourcePath stringByAppendingPathComponent:bundleName];
	NSString *customizedUIResourcesBundle = [NSBundle bundleWithPath:bundlePath];
	[self.ywIMKit setCustomizedUIResources:customizedUIResourcesBundle];
}

- (void)login: (NSString *)userId password: (NSString *)password block:(void (^)(NSError *))block {
	__weak typeof(self) weakSelf = self;
	dispatch_async(dispatch_get_global_queue(0, 0), ^{
		while (_initState != SDKInitStateSuccess) {

		}

		dispatch_async(dispatch_get_main_queue(), ^{
			[weakSelf.ywIMKit removeAllCache];
			[[weakSelf .ywIMKit.IMCore getLoginService] setFetchLoginInfoBlock:^(YWFetchLoginInfoCompletionBlock
				aComoletionBlock) {
				aCompletionBlock(YES, userId, password, nil, nil);
			}];
			//发起登录
			[[weakSelf.ywIMKit.IMCore getLoginService] asyncLoginWithCompletionBlock:^(NSError *aError, NSDictionary
				*aResult) {
				if (aError.code == 0 || [[weakSelf.ywIMKit.IMCore getLoginService] isCurrentLogined] {
					NSLog(@"登录成功")；
					if (block) {
						block(nil)
					}
				} else {
					NSLog(@"登录失败 %@", aError);
					if (block) {
						block(aError);
					}
				})
			}];
		});
	});
}






















