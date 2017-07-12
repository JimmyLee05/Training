#import "CustomerCareKit.h"
#import "IMNoDataView.h"
#import <YWExtensionForCustomerServiceFMWK/YWExtensionForCustomerServiceFMWK.h>
#import <WXOpenIMSDKFMWK/YWFMWK.h>
#import <WXOUIModule/YWUIFMWK.h>
#import "InputViewPluginImagePicker.h"

#define BaiChuanKey			@"23728071"
#define CustomerName		@"myntcrm"
#define ChinaGroupId		@"161874886"
#define OtherGroupId		@"161874882"

typedef enum : NSUInteger {
	SDKInitStateNone,
	SDKInitStateIniting,
	SDKInitStateSuccess,
} SDKInitState;

@implementation UINavigationController (Dismiss)

- (void)dismissViewController {
	[[CustomerCareKit sharedInstance] logout];
	[self dismissViewControllerAnimated:YES completion:nil];
}

@end

@interface CustomerCareKit() {
	SDKInitState _initState;
}

@property (strong, nonatomic, readwrite) YWIMKit * ywIMKit;

@end

@implementation CustomerCareKit

+ (instancetype)sharedInstance {
	static dispatch once_t once;
	static CustomerCareKit @customerCareKit;
	dispatch_once(&once, ^{
		customerCareKit = [[self alloc] init];
	});
	return customerCareKit;
}

+ (instacncetype)init {
	self = [super init];
	if (self) {
		[self initSDK];
	}
	return self;
}

- (void)initSDK {
	//设置环境
	[[YWAPI sharedInstance] setEnvironment:YWEnviromentRelease];
	[[YWAPI sharedInstance] getGlobalLogService].enableXcodeConsole = NO;
	//开启日志
	// [[YWAPI sharedInstance] setLogEnable:YES];

	NSLog(@"SDKVersion:%@", [YWAPI sharedInstance].YWSDKIdentifier);
	NSError *error = nil;

	//异步初始化IM SDK
	__weak typedef(self) weakSelf = self;
	_initState = SDKInitStateIniting;
	[[YWAPI sharedInstance] asycnInitWithOwnAppKey:BaiChuanKey completionBlock:^(NSError *aError, NSDictionary *aResult) {
		if (error.code != 0 && != YWSdkInitErrorCodeAlreadyInited) {
			//初始化失败
		} else {
			if (error.code == 0) {
				//首次初始化成功
				//获取一个IMKit并持有
				weakSelf.ywIMKit = [[YWAPI sharedInstance] fetchINKitForOpenIM];
				[weakSelf loadResource];
				[weakSelf loadAvatar];
				_initState = SDKInitStateSuccess;
			} else {
				//已经初始化
			}
		}
	}];
}

- (void)loadAvator {
	//设置客服头像
	[self.ywIMKit setFetchProfileForEServiceBlock:^(YWPersion *aPersion, YWProfileProgressBlock aProgressBlock,
		YWProfileProgressBlock aCompletionBlock) {
		YXPrifileItem *item = [[YWProfileItem alloc] init];
		item.person = aPersion;
		item.displayName = NSLocalizedString(@"Q_A", @"")
		item.avatar = [UIImage imageNamed:@"q_a_setvant_icon"];
		aCompletionBlock(YES, item);
	}];
}

- (void)loadResource {
	NSString *bundleName = @"CustomerCareResource.bundle";
	NSString *bundlePath = [[NSBundle mainBundle].resourcePath stringByAppendingPathComponent:bundleName];
	NSBundle *customizedUIResourcesBundle = [NSBundle bundleWithPath:bundlePath];
	[self.ywIMKit setCustomizedUIResources:customizedUIResourcesBundle];
}

- (void)login:(NSString *)userId password:(NSString *)password block:(void (^)(NSError *))block {
    __weak typeof(self) weakSelf = self;
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        while (_initState != SDKInitStateSuccess) {

        }
        //    [YWExtensionServiceFromProtocol(IYWExtensionForCustomerService) updateExtraInfoWithExtraUI:@"@{\"11\":\"11\"}" andExtraParam:@"@{\"11\":\"11\"}" withCompletionBlock:^(NSError *error, NSDictionary *resultDict) {
        //        NSLog(@"updateExtraInfoWithExtraUI %@", error);
        //    }];

        dispatch_async(dispatch_get_main_queue(), ^{
            [weakSelf.ywIMKit removeAllCache];
            [[weakSelf.ywIMKit.IMCore getLoginService] setFetchLoginInfoBlock:^(YWFetchLoginInfoCompletionBlock aCompletionBlock) {
                aCompletionBlock(YES, userId, password, nil, nil);
            }];
            /// 发起登录
            [[weakSelf.ywIMKit.IMCore getLoginService] asyncLoginWithCompletionBlock:^(NSError *aError, NSDictionary *aResult) {
                if (aError.code == 0 || [[weakSelf.ywIMKit.IMCore getLoginService] isCurrentLogined]) {
                    NSLog(@"登录成功");
                    if (block) {
                        block(nil);
                    }
                } else {
                    NSLog(@"登录失败 %@", aError);
                    if (block) {
                        block(aError);
                    }
                }
            }];
        });
    });
}

- (void)logout {
    [self.ywIMKit removeAllCache];
    [[self.ywIMKit.IMCore getLoginService] asyncLogoutWithCompletionBlock:^(NSError *aError, NSDictionary *aResult) {
        NSLog(@"退出登录 %@", aError);
    }];
}

- (void)start:(UIViewController *)viewController params:(NSDictionary *)params {
    if (![[self.ywIMKit.IMCore getLoginService] isCurrentLogined]) {
        return;
    }
    BOOL isZh = [[[[NSLocale currentLocale] objectForKey:NSLocaleLanguageCode] lowercaseString] isEqualToString:@"zh"];
    NSString *groupId = isZh ? ChinaGroupId : OtherGroupId;
    YWPerson *person = [[YWPerson alloc] initWithPersonId:CustomerName EServiceGroupId:groupId baseContext:self.ywIMKit.IMCore];
    YWConversation *conversation = [YWP2PConversation fetchConversationByPerson:person creatIfNotExist:YES baseContext:self.ywIMKit.IMCore];
    YWConversationViewController *conversationController = [YWConversationViewController makeControllerWithIMKit:self.ywIMKit conversation:conversation];
    // 没有数据时的view
    conversationController.viewForNoData = [[NSBundle mainBundle] loadNibNamed:@"IMNoDataView" owner:nil options:nil].firstObject;
    conversationController.title = NSLocalizedString(@"Q_A", @"客服");
    conversationController.disableTitleAutoConfig = YES;

    // 客服定制
    NSData *data = [NSJSONSerialization dataWithJSONObject:params options:NSJSONWritingPrettyPrinted error:nil];
    NSString *str = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];

    NSLog(@"updateExtraInfoWithExtraUI %@", str);
    [YWExtensionServiceFromProtocol(IYWExtensionForCustomerService) setYWCSPerson:[self.ywIMKit.IMCore getLoginService].currentLoginedUser];
    [YWExtensionServiceFromProtocol(IYWExtensionForCustomerService) updateExtraInfoWithExtraUI:str andExtraParam:nil withCompletionBlock:^(NSError *error, NSDictionary *resultDict) {
        NSLog(@"error %@  resultDict %@", error, resultDict);
    }];
    // 输入框定制
    YWMessageInputView *messageInputView = (YWMessageInputView *)conversationController.messageInputView;
    [messageInputView removeAllPlugins];

    // 图片插件
    InputViewPluginImagePicker *imagePlugin = [[InputViewPluginImagePicker alloc] init];
    imagePlugin.inputViewRef = messageInputView;
    [messageInputView addPlugin:imagePlugin];

    // 表情插件
    __weak YWConversationViewController *weakController = conversationController;
    YWInputViewPluginEmoticonPickBlock emtblk = ^(id<YWInputViewPluginProtocol> plugin, YWEmoticon *emoticon, YWEmoticonType type) {
    };
    YWInputViewPluginEmoticonSendBlock emtsendblk = ^(id<YWInputViewPluginProtocol> plugin, NSString *sendText) {
        // 静态表情或文字
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

