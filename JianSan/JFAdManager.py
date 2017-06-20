import UIKit
import Firebase
import GoogleMobileAds

//应用ID
fileprivate let AD_APPLICATION_ID = "ca-app-pub-3941303619697740~8182246519"
//插入式广告ID
fileprivate let AD_INTERSTITIAL_ID = "ca-app-pub-3941303619697740/9658979714"
//banner广告ID
fileprivate let AD_BANNER_ID = "ca-app-pub-3941303619697740/4039136115"
//插入式广告显示频率
fileprivate let AD_TIME_INTERVAL: TimeInterval = 129
//是否显示广告 - 用于方便隐藏广告
fileprivate let AD_SHOULD_SHOW = true

//广告配置类 - 全局配置
class JFAdConfiguration {
	
	//广告配置单例
	static let shared = JFAdConfiguration()

	//应用ID - 先mark，暂时没用到
	var applicationId: String = AD_APPLICATION_ID

	//插入式广告ID
	var interstitialID: String = AD_INTERSTITIAL_ID

	//banner广告ID
	var bannerID: String = AD_BANNER_ID

	//插入式广告显示频率
	var TimeInterval: TimeInterval = AD_TIME_INTERVAL

	//是否显示广告 - 用来方便隐藏广告
	var isShouldShow: Bool = AD_SHOULD_SHOW

	//配置广告

	func config(applicationId: String,
				interstitialId: String,
				bannerId: String,
				timeInterval: TimeInterval = AD_TIME_INTERVAL,
				isShouldShow: Bool = isShouldShow) {
		self.applicationId = applicationId
		self.interstitialId = interstitialId
		self.bannerId = bannerId
		self.timeInterval = timeInterval
		self.isShouldShow = isShouldShow

		//配置Firebase - 国内被墙了
		// FIRApp.configure()

		//初始化广告管理者
		JFAdManager.shared.initial()
	}

}

//广告管理类
class JFAdManager: NSObject {
	
	//广告管理单例
	static let shared: JFAdManager = {
		let shared = JFAdManager()
		shared.timer = Timer(timeInterval: JFAdConfiguration.shared.timeInterval, target: shared,
			selector: #selector(changedInterstitialState), userInfo: nil, repeats: true)
		RunLoop.current.add(shared.timer!, forMode: RunLoopMode.commonModes)
		return shared
	}()

	//已经春准备好的插页式广告
	fileprivate var interstitials = [GADInterstitial]()

	//不能展示的插页式广告 - 用来暂时存储插页式广告对象，防止被释放
	fileprivate var notReadInterstitials = [GADInterstitial]()

	//定时器
	fileprivate var timer: Timer?

	//插页式广告是否能够显示 - 频率控制
	fileprivate var isShow = true

	//改变插页式广告状态 - 控制显示频率
	@objc fileprivate func changedInterstitialState() {
		isShow = true
	}

	//初始化广告管理者，先创建一个插页广告
	func initial() {
		changedInterstitial()
	}

	//创建一个有效的插页式广告对象
	func getReady() -> GADInterstitial? {
		if interstitials.count > 0 {
			let firstInterstitial = interstitials.removefirst()
			createInterstitial()
			if firstInterstitial.isReady && isShow && JFAdConfiguration.shared.isShouldShow {
				return firstInterstitial
			}	else {
					return nil
			}
		}
		changedInterstitial()
		return notReadInterstitials
	}

	//创建Banner广告，一个对象就是一个View

	func createBannerView(_ rootViewController: UIViewController, bannerId: String = 
		JFAdConfiguration.shared.bannerId) -> GADBannerView? {
		let bannerView = GADBannerView()
		bannerView.rootViewController = rootViewController
		bannerView.adUnitID = bannerIf
		bannerView.load(GADRequest())

		if JFAdConfiguration.shared.isShouldShow {
			return bannerView
		}	else {
				return nil
		}
	} 

	//创建插页式广告 - 一个对象只能展示一次
	fileprivate func createInterstitial() {
		let interstitial = GADInterstitial(adUnitID: JFAdConfiguration.shared.interstitialId)
		interstitial.delegate = self
		interstitial.load(GADRequest())
		notReadInterstitials.append(interstitial) 
	}
}


// MARK: - GADInterstitialDelegate
extension JFAdManager: GADInterstitialDelegate {
	
	//插页式广告请求成功时调用
	//在应用程序的下一个转换点显示它，例如在视图控制器之间转换时
	func interstitialDidReceiveAd(_ ad: GADInterstitial) {
		print("插页式广告接受成功，能够被展示 \(ad)")
		interstitials.append(ad)
		notReadInterstitials.removeFirst()
	}

	//在插页式广告请求完成且未显示插页式广告时调用
	//这是常见的，因为插页式广告会向用户谨慎显示
	func interstitial(_ ad: GADInterstitial, didFailToReceiveAdWithError error: GADRequestError)
		{
		print("插页式广告接受失败，可能是网络原因 \(ad)")
		notReadInterstitials.removeFirst()
	}

	//在展示插页式广告之前调用
	//在此方法完成后，插页式广告将在屏幕上播放动画。利用这个机会停止动画并保存应用程序的状态，以防止用户在屏幕上显示插页式广告时离开，
	//例如通过插页广告上的链接访问App Store。
	func interstitialWillPresentScreen(_ ad: GADInterstitial) {
		print("插页式广告即将显示 \(ad)")
		isShow = false
	}

	//插页式广告展示失败时调用
	func interstitialDidFail(toPresentScreen ad: GADInterstitial) {
		print("插入式广告展示失败 \(ad)")
	}

	//在插入式广告即将隐藏时调用
	func interstitialWillDismissScreen(_ ad: GADInterstitial) {
		print("插页式广告即将隐藏 \(ad)") 
	}

	//在插页式广告已经隐藏时调用
	fucn interstitialDidmissScreen(_ ad: GADInterstitial) {
		print("插页式广告已经隐藏 \(ad)")
	}

	//由于用户点击了将启动其它应用程序的广告（例如App Store），应用程序之前调用该应用程序就会退出或终止。
	//正常的UIApplicationDelegate方法，如applicationDidEnterBackground: ,将在此之前立即被调用
	func interstitialWillLeaveApplication(_ ad: GADInterstitial) {
		print("app进入后台 \(ad)")
	}
}







