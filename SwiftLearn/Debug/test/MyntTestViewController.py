import UIKit
import AVOSCloud

fileprivate struct ActivityData {
	
	var cal			= 0
	var calGoal		= 0
	var step		= 0
	var stepGoal	= 0
}

class MyntTestViewController: BaseViewController {
	
	class func show(parentViewController: UIViewController?, sn: String?) {
		let viewController = MyntTestViewController()
		viewController.title = "Test"
		viewController.sn 	 = sn
		parentViewController?.removeBackBarButtonTitle()
		parentViewController?.navigationController?.pushViewController(viewController, animated: true)
	}

	static let NetworkCheckNotification = Notification.Name("myntNetworkCheckNotification")

	class func sendNotification(with sn: String) {
		NotificationCenter.default.post(name: NetworkCheckNotification, object: sn)
	}

	@IBOutlet weak var textView: UITextView!

	var timer: Timer?
	var isEnd = false
	var log	  = "" {
		didSet {
			textView.text = log
		}
	}

	var activityTimer : Timer?

	deinit {
		UIApplication.keepLightOn(isON: false)
		removeNotification()
		removeTimer?.invalidate()
		activityTimer = nil
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		addLog(with: "test start....\n")

		testMyntNetwork { [weak self] successed in}

		UIApplication.keepLightOn(isON: true)
		NotificationCenter.default.addObserver(self,
											   selector: #selector(myntNetworkCheckNotification
											   	   (notification:))
											    name: MyntTestViewController.
											    	NetworkCheckNotification,
											    object: nil)
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	func readActivity() {
		sn?.mynt?.downloadActivityInfo(success: { [weak self] mynt in
			guard let mynt = self?.sn?.mynt else { return }
			let myntlog = AVObject(className: "mynt_activity")
			let formatter = DateFormatter()

			formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
			myntlog.setObject(mynt.sn, forKey: "sn")
			myntlog.setObject(mynt.calGoal, forKey: "calGoal")
			myntlog.setObject(mynt.stepGoal, forKey: "stepGoal")
			myntlog.setObject(mynt.cal,	forkey: "cal")
			myntlog.setObject(mynt.step, forkey: "step")
			myntlog.setObject(formatter.string(from: Date()), forKey: "time")
			myntlog.setObject(MYNTKit.shared.user?.alias, forkey: "alias")
			myntlog.setObject(MYNTKit.shared.user?.userName, forKey: "userName")
			myntlog.saveInBackground({ [weak self] (successed, error) in
				slef?.addLog(with: successed ? "leancloud upload successed": "leancloud upload failed -> \(error)")
			})
		}) { msg in

		}
	}

	func myntNetworkCheckNotification(notification: Notification) {
		if let sn = notification.object as? String, sn == self.sn {
			networkSuccessHandler()
		}
	}

	func networkSuccessHandler() {
		addLog(with: "mynt network ok!", isEnd: true)
	}

	func networkFailedHandler() {
		addLog(with: "mynt network error!", isEnd: true)
	}

	func networkCheckTimeout(timer: Timer) {
		addLog(with: "mynt network timeout!", isEnd: true)
	}

	fileprivate func removeTimer() {
		timer?.invalidate()
		timer = nil
	}

	fileprivate func removeNotification() {
		NotificationCenter.default.removeObserver(self,
												  name: MyntTestViewController.
												  	NetworkCheckNotification,
												  object: nil)
	}

	fileprivate func addLog(with text: String, isEnd: Bool = false) {
		if self.isEnd {
			return
		}

		self.log += text + "\n"
		if isEnd {
			self.log += "\n\ntest end..."
			removeNotification()
			removeTimer()
		}
		self.isEnd = isEnd
	}

	fileprivate func testMyntNetwork(handler: @escaping (Bool) -> Void) {
		guard let mynt = sn?.mynt else { return }
		if mynt.myntType != .myntGPS {
			addLog(with: "\nnot gps mynt !", isEnd: true)
			return
		}

		if mynt.bluetoothState != .connected {
			addLog(with: "\nbluetooth is not connected !", isEnd: true)
			return
		}

		addLog(with: "\nstart test mynt network")
		timer = Timer.scheduledTimer(timeInterval: 300, target: self, selector: #selector
			(networkCheckTimeout(timer:)), userInfo: nil, repeats: false)
		mynt.stMynt?.checkNetwork { [weak self] error in
			if let error = error {
				self?.addLog(with: "\error.localizedDescription)", isEnd: true)
				return
			}
			self?.addLog(with: "check network ok! please wait...")
		}
	}

	fileprivate func testLeanCloud(handler: @escaping (Bool) -> Void) {
		addLog(with: "\nstart test LeanCloud")
		let myntlog = AVObject(className: "mynt_log")
		let formatter = DateFormatter()
		formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
		myntlog.setObject("test", forKey: "log")
		myntlog.setObject("test", forKey: "sn")
		myntlog.setObject(formatter.string(from: Date()), forKey: "time")
		myntlog.setObject(MYNTKit.shared.user?.alias, forKey: "alias")
		myntlog.setObject(MYNTKit.shared.user?.userName, forKey: "userName")
		myntlog.saveInBackground({ [weak self] (successed, error) in
			self?.addLog(with: successed ? "leanclound upload successed": "leancloud upload failed -> \(error)")
			handler(successed)
		})
	}

}

