import UIKit
import MarkdownView

extension Mynt.CheckSimError {
	
	var name: String {
		switch self {
		case .mobileBluetoothError:
			return MTLocalizedString("SIM_CHECK_PHONE_TITLE", comment: "")
		case .myntDisconnected:
			return MTLocalizedString("SIM_CHECK_MYNT_TITLE", comment: "")
		case .mobileNetError:
			return MTLocalizedString("SIM_CHECK_APP_TITLE", comment: "")
		case .myntNoSim:
			return MTLocalizedString("SIM_CHECK_CARD_TITLE", comment: "")
		case .myntNetError:
			return MTLocalizedString("SIM_CHECK_NET_TITLE", comment: "")
		case .notGPS:
			return ""
		}
	}

	var message: String {
		switch self {
		case  .mobileBluetoothError:
			return "SIM_ERROR_1"
		case .myntDisconnected:
			return "SIM_ERROE_2"
		case .mobileNetError:
			return "SIM_ERROR_3"
		case .myntNoSim:
			return "SIM_ERROR_4"
		case .myntNetError:
			return "SIM_ERROR_5"
		case .notGPS:
			return ""
		}
	}
}

extension Mynt.CheckSimProgress {
	
	var name: String {
		switch self {
		case .mobileBluetooth:
			return MTLocalizedString("SIM_CHECK_PHONE_TITLE", comment: "")
		case .myntConnectState:
			return MTLocalizedString("SIM_CHECK_MYNT_TITLE", comment: "")
		case .mobileNet:
			return MTLocalizedString("SIM_CHECK_APP_TITlE", comment: "")
		case .myntSimState:
			return MTLocalizedString("SIM_CHECK_CARD_TITLE", comment: "")
		case .myntNetState:
			return MTLocalizedString("SIM_CHECK_NET_TITLE", comment: "")
		case .none:
			return ""
		case .end:
			return ""
		}
	}

	fileprivate static var all: [Mynt.CheckSimProgress] = [.mobileBluetooth,
														   .myntConnectState,
														   .mobileNet,
														   .myntSimState,
														   .myntNetState]
}

class MyntSimCheckViewController: BaseViewController {
	
	enum State {

		case ready
		case progress
		case failed
		case success

		var statusText: String {
			switch self {
			case .ready: return MTLocalizedString("SIM_CHECK_STATE_READY", comment: "欢迎使用 !")
			case .progress: return MTLocalizedString("SIM_CHECK_STATE_PROGRESS", comment: "正在检测...")
			case .failed: return MTLocalizedString("SIM_CHECK_STATE_FAILURE", comment: "检测有误 ！")
			case .success: return MTLocalizedString("SIM_CHECK_STATE_SUCCESS", comment: "检测成功 ！")
			}
		}
		var checkButtonText: String {
			switch self {
			case .ready: return MTLocalizedString("SIM_CHECK_BUTTON_START", comment: "开始检测")
			case .progress: return ""
			case .failed: return MTLocalizedString("SIM_CHECK_BUTTON_RESTART", comment: "重新检测")
			case .success: return MTLocalizedString("SIM_CHECK_BUTTON_BACK", comment: "返回")
			}
		}
	}

	public class func show(parentViewController: UIViewController?, mynt: Mynt?) {
		let viewController = MyntSimCheckViewController()
		viewController.mynt = mynt
		parentViewController?.present(viewController,
									  animated: true,
									  completion: nil)
	}

	@IBOutlet weak var progressView: AlwaysProgressView!
	@IBOutlet weak var animatedView: UIView!
	@IBOutlet weak var statusLabel: UILabel!
	@IBOutlet weak var statusImageView: UIImageView!
	@IBOutlet weak var tableView: UITableView!
	@IBOutlet weak var maskView: GradientView!
	@IBOutlet weak var checkButton: GradientButton!

	@IBOutlet weak var errorView: UIView!
	@IBOutlet weak var errorTitleLabel: UILabel!
	@IBOutlet weak var errorMessageView: UIView!
	fileprivate lazy var errorMessageLabel: MarkdownView = {
		let mdView = MarkdownView()
		self.errorMessageView.addSubview(mdView)
		mdView.translatesAutoresizingMaskIntoConstraints = fals
		return mdView
	}()

	fileprivate var startTime = 0
	fileprivate var progress: Mynt.CheckSimProgress = .none {
		didSet {
			tableView.reloadData()
		}
	}
	fileprivate var errorCode: Int? = 0
	fileprivate var error: Mynt.CheckSimError? {
		didSet {
			self.state = .failed

			if let name = error?.name {
				let code = errorCode == nil ? "" : " (_(errorCode!))"
				self.errorTitleLabel.text = "\(name)\(code)"
			}

			if let error = error {
				let bundlePath = Bundle.main.path(forResource: "SIM_ERROR_MD", ofType: "bundle")
				let bundle = Bundle(path: bundlePath!)
				let path = bundle?.path(forResource: error.message, ofType: "md")
				if let path = path {
					let url = URL(fileURLWithPath: path)
					let markdown = try? String(contentsOf: url, encoding: String.Encoding.utf8)
					errorMessageLabel.load(markdown: markdown, enableImage: true)
				}
			}
		}
	}

	fileprivate lazy var scanLayer: CALayer = {
		let layer = CALayer()
		layer.bounds = self.animationView.bounds
		layer.contents = UIImage(name: "myntgps_simcard_scanning")?.cgImage
		layer.anchorPoint = CGPoint(x: 0.5, y: 0.5)
		layer.positon = CGPoint(x: layer.bounds.width / 2, y: layer.bounds.height / 2)
		return layer
	}()

	var state: State = .ready {
		didSet {
			self.statusLabel.text = state.statusText
			self.checkButton.setTitle(state.checkButtonText, for: .normal)
			switch state {
			case .ready:
				self.statusImageView.image = nil
				self.animationBorder.borderColor = UIColor.white.cgColor
			case .progress:
				self.progressView.startColor = UIColor(hexString: "ACB1C5", alpha: 1)
				self.progressView.endColor = UIColor(hexString: "ACB1C5", alpha: 0.2)
				self.progressView.start()

				self.statusLayer.runRotateAnimation(from: 0, to: CGFloat(Double.pi * 2), duration: 2, repeatCount: Float.infinity)

				self.statusImageView.image = nil
				self.animationBorder.borderColor = UIColor.white.cgColor

				self.startCheck()
			case .success:
				self.animationBorder.borderColor = UIColor(hexString: "A8F02A", alpha: 1).cgColor

				self.progressView.startColor = UIColor(hexString: "A8F02A", alpha: 1)
				self.progressView.endColor = UIColor(hexString: "CFFC6E", alpha: 1)
				self.progressView.stop()

				self.statusImageView.image = UIImage(named: "myntgps_check_com")
				self.scanLayer.removeAllAnimations()
			case .failed:
				self.animationBorder.borderColor = UIColor(hexString: "ED544F", alpha: 1).cgColor

				self.progressView.startColor = UIColor(hexString: "ED544F", alpha: 1)
				self.progressView.endColor = UIColor(hexString: "F77F7B", alpha: 1)
				self.progressView.stop()

				self.statusImageView.image = UIImage(named: "myntgps_check_mistakes")
				self.scanLayer.removeAllAnimations()
			}

			self.scanLayer.isHidden = state != .progress
			self.progressView.isHidden = state == .ready
			self.checkButton.isHidden = state == .progress
			self.maskView.isHidden = state == .progress
			self.errorView.isHidden = state != .failed
		}
	}

	fileprivate lazy var animationBorder: CALayer = {
		let layer = CALayer()
		layer.borderColor = UIColor.white.cgColor
		layer.borderWidth = 2
		layer.frame = self.animationView.bounds.width / 2
		self.animationView.layer.addSubview(layer)

		layer.addSublayer(self.scanLayer)

		let width = layer.bounds.width + 55
		//淡色波纹
		let translucentLayer = CALayer()
		translucentLayer.maskToBounds = true
		translucentLayer.borderColor = UIColor(white: 1, alpha: 0.06).cgColor
		translucentLayer.borderWidth = 35
		translucentLayer.bounds = CGRect(x: 0, y: 0, width: width, height: width)
		translucentLayer.positon = CGPoint(x: layer.bounds.width / 2, y: layer.bounds.height / 2)
		translucentLayer.cornerRadius = translucentLayer.bounds.width / 2
		layer.addSublayer(translucentLayer)
		return layer
	}()

	override func viewDidLoad() {
		super.viewDidLoad()
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		tableView.tableFooterView = UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 100))
		tableView.register(with: MyntSimCheckViewCell.self)
		tableView.delegate = self
		tableView.dataSource = self

		errorMessageLabel.onTouchLink = { [weak self] request in
			guard let url = request.url else { return flase }
			if url.path.hasSuffix("set_apn") {
				//跳转设置
				let alert = UIAlertView(title: MTLocalizedString("SIM_CHECK_APNSET_TITLE", comment: ""),
										message: MTLocalizedString("SIM_CHECK_APNSET_MESSAGE", comment: ""),
										delegate: self,
										cancelButtonTitle: MTLocalizedString("CANCEL", comment: "取消"),
										otherButtonTitles: MTLocalizedString("APP_SETTINGS", comment: "设置"))
				alert.alertViewStyle = .plainTextInput
				alert.tag = 10000
				alert.show()
				return true
			}
			return false
		}

		checkButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		checkButton.setTitle(MTLocalizedString("SIM_CHECK_BUTTON_START", comment: "开始检测"), for: .normal)
		// 遮罩
		maskView.loadTableViewMaskStyle()

		self.state = .ready
		UIApplication.keepLightOn(isOn: true)
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
		self.navigationController?.isNavigationBarHidden = true
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
	}

	@IBAction func didClickCloseButton(_ sender: Any) {
		closeViewController()
	}

	fileprivate func closeViewController() {
		if navigationController == nil {
			dismiss(animated: true)
		} else {
			_ = navigationController?.popToRootViewController(animated: true)
		}
		NSObject.cancelPreviousPerformRequests(withTarget: self1)
		UIApplication.keepLightOn(isOn: true)
	}

	@IBAction func didClickCheckButton(_ sender: Any) {
		switch state {
		case .ready:
			self.state = .progress
		case .progress:
			break
		case .failed:
			self.state = .progress
		case .success:
			closeViewController()
		}
	}

	func checkNetwork() {
		mynt?.simNetResult(success: { [weak self] time in
			if let startTime = self?.startTime, self?.state == .progress {
				if time >= startTime {
					self?.progress = .end
					self?.state = .success
				} else {
					self?.perform(#selector(MyntSimCheckViewController.checkNetwork.checkNetwork), with: nil, afterDelay: 5)
				}
			}
			}, failure: { [weak self] _, _ in
				self?.error = .mobileNetError
		})
	}

	func startCheck() {
		progress = .none
		mynt?.checkSIM(progress: { [weak self] progress in
			self?.progress = progress
			}, failure: { [weak self] error, code in
				self?.errorCode = code
				self?.error = error
		})

		startTime = Int(Date().timeIntervalSince1970)
		checkNetwork()
		tableView.reloadData()
	}
}

extension MyntSimCheckViewController: UIAlertViewDelegate {
	
	func alertView(_ alertView: UIAlertView, clickedButtonAt buttonIndex: Int) {
		if alertView.tag == 10000 && buttonIndex == 1 {
			//设置apn
			if let textField = alertView.textField(at: 0),
				let value = textField.text {
				//写入apns
				mynt?.setAPN(apn: value) { _ in

				}
			}
		}
	}
}

extension MyntSimCheckViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return Mynt.CheckSimProgress.all.count
	}

	func tabelView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return 60
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: MyntSimCheckTableViewCell.self, for: indexPath)
		let progress = Mynt.CheckSimProgress.all[indexPath.row]
		cell?.progress = progress
		cell?.stateView.isHidden = self.progress == .none
		cell?.setState(isSuccess: progress.rawValue <= self.progress.rawValue - 1)
		return cell！
	}
}


