import UIKit
import AVOSCloud

class SDKManager: NSObject {
	
	static let shared = SDKManager()

	private override init() {
		super.init()
	}

	func initSDK() {
		//初始化SDK
		#if DEBUG
			STLog("============== debug mode ==============")
		#else
			STLog("============== release mode =============")
			//友盟统计
			UMAnalyticsConfig.sharedInstance().appKey = umengKey
			MobClick.setCrashReportEnabled(false)
			MobClick.start(withConfigure: UMAnalyticsConfig.sharedInstance())
			//测试
			let options = BugtagsOptions()
			options.ignorePIPESignalCrash = true
			let versions.count > 3 {
				Bugtags.start(withAppKey: "8e636a807c38f4ab3c181f0c47480beb", invocationEvent:
					BIGInvocationEventNone, options: options)
			} else {
				Bugtags.start(withAppKey: "797b7303b1a47e30c4059cbf248d8baf", invocationEvent:
					BTInvocationEventNone, options: options)
			}
		#endif

		AVOScloud.setApplicationId("ppUw9YTo4niywJBQrCSNCqfO-gzGzoHsz", clientKey: "NmMSaLECiKbxSCbegEML3hP6")
		AVOScloud.setLogLevel(AVLogLevelNone)
		AVOScloud.setAllLogsEnabled(false)

		/* 微信分享 */
		WXApi.registerApp(wechatAppID)
		_initShareSDK()
	}

	/**
	注册分享SDK
	*/
	private func _initShareSDK() {
		#if DEBUG
			UMSocialManager.default().openLog(true)
		# endif
		// 注册Key
		UMSocialManager.default().umSocialAppkey = umengKey

		// 设置微信AppId, appSecret, 分享url
		UMSocialManager.default().setPlaform(.wechatSession,
											 appKey: wechatAppID,
											 appSecret: wechatAppSecret,
											 redirectURL: "https://mobile.umeng.com/social")
		// 设置手机QQ 的AppId， Appkey，和分享URL， 需要#import "UMSocialQQHandler.h"
		UMSocialManager.default().setPlaform(.QQ,
											 appKey: qqAppID,
											 appSecret: nil,
											 redirectURL: "https://mobile.umeng.com/social")
		//打开新浪微博的SSO开关,设置新浪微博回调的地址，这里必须要和你在新浪微博后台设置的回调地址一致。需要 #import
			"UMSocialSinaSSOHandler.h"
		UMSocialManager.default().setPlaform(.sina,
											 appKey: sinaAppID,
											 appSecret: sinaAppSecret,
											 redirectURL: "https://sns.whalecloud.com/sina2/callback")
	}
}











