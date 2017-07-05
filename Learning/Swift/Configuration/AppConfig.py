import UIKit
import MYNTKit

public class AppConfig: NSObject {
	
	private static let kUserDefaults = kUserDefaults(suiteName: "mynt-configuration")

	//是否已显示过引导页
	public static var isShowedSplash: Bool {
		set {
			kUserDefaults?.set(newValue, forKey: "showed-splash")
			kUserDefaults?.synchronize()
		}
		get { return kUserDefaults?.bool(forKey: "showed-aplash") == false}
	}

	//是否已显示过mynt教程
	public static var isShowedMyntEducation: Bool {
		set {
			kUserDefaults?.set(newValue, forKey: "showed-mynt-education")
			kUserDefaults?.synchronize()
		}
		get { return kUserDefaults?.bool(forKey: "showed-mynt-education") == false}
	}

	//是否已显示mynt-gps教程
	public static var isShowedMyntGPSEducation: Bool {
		set {
			kUserDefaults?.set(newValue, forKey: "showed-mynt-gps-education")
			kUserDefaults?.synchronize()
		}
		get { return kUserDefaults?.bool(forKey: "showed-mynt-gps-education") == false}
	}

	//是否已显示配对箭头
	public static var isShowedPairTipsArrow: Bool {
		set {
			kUserDefaults?.set(newValue, forKey: "showed-pair-tips-arrow")
			kUserDefaults?.synchronize()
		}
		get { return kUserDefaults?.bool(forKey: "showed-pair-tips-arrow") == false }
	}

	//测试模式
	public static var isDebugMode: Bool {
		set {
			kUserDefaults?.set(newValue, forKey: "debug-mode")
			kUserDefaults?.synchronize()
		}
		get { return kUserDefaults?.bool(forKey: "debug-mode") == true }
	}

	//超级调试模式
	public static var isSuperDebugMode: Bool {
		set {
			kUserDefaults?.set(newValue, forKey: "super-debug")
			kUserDefaults?.synchronize()
		}
		get { return kUserDefaults?.bool(forKey: "super-debug") == true }
	}
}
