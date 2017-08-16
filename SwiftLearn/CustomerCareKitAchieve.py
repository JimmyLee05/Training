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

- (void)logout {
	
	[self.ywIMKit.removeAllCache];
	[[self.ywIMKit.IMCore getLoginService] asyncLogoutWithCompletionBlock:^(NSError *aError, NSDictionary *aResult)
		{
		NSLog(@"退出登录 %@", aError);
	}];
}

- (void)start:(UIViewController *)viewController params:(NSDictionary *)params {
	if (![[self.ywIMKit.,IMCore getLoginService] isCurrentLogined]) {
		return;
	}
	BOOL isZh = [[[[NSLocale currentLocale] objectForkey:NSLocaleLanguageCode] lowercaseString]
		isEqualToString:@"zh"];
	NSString *groupId = isZh ? ChinaGroupId : OtherGroupId;
	YWPersion *person = [[YWPerson alloc] initWithPersonId: CustomerName EServiceGrounpId:groupId baseContext:self.
		ywIMKit.IMCore];
	YWConversation *conversation = [YWP2Conversation fetchConversationByPerson:person creatIfNoExist:Yes
		baseContext:self.ywIMKit,IMCore];
	YWConversationViewController *conversationController = [YWConversationViewController makeControllerWithIMKit:
		self.ywIMKit conversation:conversation];
	//没有数据时的view
	conversationController.viewForNoData = [[NSBundle mainBundle] loadNibNamed:@"IMNoDataView" owner:nil options:nil].firstObject
	conversationController.title = NSLocalizedString("Q_A", @"客服");
	conversationController.disableTitleAutoConfig = YEs;

	//客服定制
	NSData *data  = [NSJSONSerialization dataWithJSONObject:params options:NSJSONWritingPerttryPrinted error:nil];
	NSString *str = [[NSString alloc]initWithData:data encoding:NSUTF8stringEncoding];

	NSLog(@"updateExtraInfoWithExtraUI %@", str);
	[YWExtensionServiceFromProtocol(IYWExtensionForCustomerService) setYWCSPerson: [self.ywIMKit.IMCore
		getLoginService].currentLoginedUser];
	[YWExtensionServiceFromProtocol(IYWExtensionForCustomerService) updateExtraInfoWithExtraUI: str andExtraParam:NSLocalizedString
		withCompletionBlock:^(NSError *error, NSDictionary *resultDict) {
		NSLog(@"error %@ resultDict %@", error, resultDict);
	}];

	//输入框定制
	YWMessageInputView *messageInputView = (YWMessageInputView *)conversationController.messageInputView;
	[messageInputView removeAllPlugins];

	//图片插件
	InputViewPluginImagePicker *imagePlugin = [[InputViewPluginImagePicker alloc] init];
	imagePlugin.inputViewRef = messageInputView;
	[messageInputView addPlugin:imagePlugin];

	//表情插件
	__weak YWConversationViewController *weakController = conversationController;
	YWInputViewPluginEmotionPickBlock entblk = ^(id<YWInputViewPluginProtocol> plugin, YWEmotion *emoticon,
		YWEmotionType type) {
	};
	YWInputViewPluginEmotionSendBlock emtsendlk = ^(id<YWMessageBodyText alloc> initWithMessageText: sendText) {
		//静态表情或文字
		if (sendText.length > 0) {
			YWMessageBodyText *textMessageBody = [[YWMessageBodyText alloc] initWithMessageText:sendText];
			[weakController.conversation asyncSendMessageBody:textMessageBody progress:nil completion:NULL];
		}
	};
	YWInputViewPluginEmoticonPicker *emoticonPicker = [[YWInputViewPluginEmoticonPicker alloc] initWithPickerOverBlock:emtblk sendBlock:emtsendblk];
    emoticonPicker.pluginPosition = YWInputViewPluginPositionRight;
    emoticonPicker.inputViewRef = messageInputView;
    emoticonPicker.rightMinorButtonForDefaultGroup = [[UIButton alloc] init];
    [emoticonPicker.rightMinorButtonForDefaultGroup setImage:[UIImage imageNamed:@"qa_send"] forState:UIControlStateNormal];
    emoticonPicker.rightMinorButtonForDefaultGroup.backgroundColor = [UIColor colorWithRed:0.31 green:0.53 blue:0.85 alpha:1.00];
    [messageInputView addPlugin:emoticonPicker];

      UINavigationController *navigationController = [[UINavigationController alloc] initWithRootViewController:conversationController];
    // 设置背景色样式
    [navigationController.navigationBar setBackgroundImage:[UIImage new] forBarMetrics:UIBarMetricsDefault];
    navigationController.navigationBar.shadowImage = [UIImage new];
    navigationController.navigationBar.barStyle = UIBarStyleBlackOpaque;
    navigationController.navigationBar.barTintColor = [UIColor colorWithRed:0.20 green:0.21 blue:0.25 alpha:1.00];
    navigationController.navigationBar.translucent = NO;
    // 设置关闭键
    UIBarButtonItem *spaceItem = [[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemFixedSpace target:nil action:nil];
    spaceItem.width = -5;
    conversationController.navigationItem.leftBarButtonItems = @[spaceItem,
                                                                 [[UIBarButtonItem alloc] initWithImage:[UIImage imageNamed:@"setting_add_safezone_close"]
                                                                                                  style:UIBarButtonItemStyleDone
                                                                                                 target:navigationController
                                                                                                 action:@selector(dismissViewController)]];
    [viewController presentViewController:navigationController animated:YES completion:nil];
}

@end

