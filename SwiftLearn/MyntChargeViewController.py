import UIKit
import MYNTKit
import SlightechKit
import RealmSwift

public enum PayType: Int {
	
	case wechatPay
	case aliPay
	case none

	var image: UIImage? {

		switch self {
		case .wechatPay:
			return UIImage(named: "app_settings_payment_wechat")
		case .aliPay:
			return UIImage(named: "app_settings_payment_alipay")
		case .none:
			return UIImage(named: "")
		}
	}

	var payName: String {

		switch self {
		case .wechatPay:
			return NSLocalizedString("GPS_CHARGE_WECHAT", comment: "微信支付")
		case .aliPay:
			return NSLocalizedString("GPS_CHARGE_ALI", comment: "阿里支付")
		case .none:
			return ""
		}
	}
}

class MyntChargeViewController: BaseViewController, UIScrollViewDelegate {
	
	public class func show(parentViewController: UIViewController?, sn: String?) {
		let viewController 		= MyntChargeViewController()
		viewController.sn 		= sn
		parentViewController?.present(BaseNavigationController(rootViewController: viewController),
									  animated: true,
									  completion: nil)
	}

	@IBOutlet weak var scrollView: UIScrollView!
	@IBOutlet weak var infoView: UIView!
	@IBOutlet weak var avatarImageView: UIImageView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var remainderHintLabel: UILabel!
	@IBOutlet weak var remainderNumLabel: UILabel!
	@IBOutlet weak var remainderUintLabel: UILabel!
	@IBOutlet weak var remainderTimeLabel: UILabel!

	@IBOutlet weak var package1View: UIView!
	@IBOutlet weak var package2View: UIView!
	@IBOutlet weak var package3View: UIView!

	@IBOutlet weak var alipayView: UIView!
	@IBOutlet weak var wechatView: UIView!

	@IBOutlet weak var chargeButton: GradientButton!

	lazy var indoBackgroundLayer: CALayer = {
		let layer = CALayer()
		layer.backgroundColor = navigationBarColor.cgColor
		layer.anchorPoint = .zero
		self.infoView.layer.insertSublayer(layer, at: 0)
		return layer
	}()

	var payType: PayType = .aliPay {
		didSet {
			alipayView.viewWithTag(102)?.layer.borderWidth = payType == .aliPay ? 0 : 1
			wechatView.viewWithTag(102)?.layer.borderWidth = payType == .wechatPath ? 0 : 1
			(alipayView.viewWithTag(102) as? UIImageView)?.image = payType == .aliPay ? UIImage(named: "tick") : nil
			(wechatView.viewWithTag(102) as? UIImageView)?.image = payType == .wechatPay ? UIImage(named: "tick") : nil
		}
	}

	var packagesView: [UIView] {
		return [package1View, package2View, package3View]
	}
	var paysView: [UIView] {
		return [alipayView, wechatView]
	}

	var selectedPackage: SCPay.SCPackage? {
		didSet {
			packagesView.forEach { view in
				let textColor = view.tag == selectedPackage?.month ?
					UIColor(red:0.65, green:0.93, blue:0.15, alpha:1.00) :
					UIColor(red:0.65, green:0.93, blue:0.15, alpha:1.00)

				let borderColor = view.tag == selectedPackage?.month ?
					UIColor(red:0.65, green:0.93, blue:0.15, alpha:1.00) :
					UIColor(red:0.65, green:0.93, blue:0.15, alpha:1.00)

				(view.viewWithTag(101) as? UILabel)?.textColor = textColor
				(view.viewWithTag(102) as? UILabel)?.textColor = textColor
				(view.viewWithTag(103) as? UILabel)?.textColor = textColor
				view.layer.borderColor = borderColor.cgColor

			}
		}
	}

	var package: [SCPay.SCPackage] = [] {
		didSet {
			if package.count == packageView.count {
				for i in 0..<packageView.count {
					let package = packages[i]
					let packageView = packagesView[i]

					packageView.tag = package.month
					packageView.isHidden = false
					(packageView.viewWithTag(101) as? UILabel)?.text = String(format: "%.2f", package.money)
					(packageView.viewWithTag(103) as? UILabel)?.text = "\(package.month)" + NSLocalizedString("GPS_CHARGE_MONTH", comment: "月")
				}
				selectedPackage = packages.first
			}
		}
	}

	override var isNeedAddMyntNotification: Bool {
		return true
	}

	override var isShowBackgroundLayer: Bool {
		return false
	}

	override func viewDidLoad() {
		super.viewDidload()

		title = NSLocalizedString("GPS_CHARGE_TITLE", comment: "支付")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone-close"))
		setRightBarButtonItem(title: NSLocalizedString("充值记录", comment: ""))

		scrollView.delegate = self
		chargeButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		infoBackgroundLayer.frame = CGRect(x: 0, y: 0, width: self.view.frame.width, height: infoView.frame.maxY)
		packagesView.forEach { view in
			view.isHidden = true
			view.layer.cornerRadius = 4
			view.layer.borderWidth = 1
			view.layer.borderColor = UIColor(red:0.82, green:0.82, blue:0.82, alpha:1.00).cgColor
			view.isUserInteractionEnabled = true
			view.addGestureRecognizer(UITapGestureRecognizer(target: self,
															 action: #selector(MyntChargeViewController.didClickPackageView(gestureRecognizer:))))
		}

		(alipayView.viewWithTag(101) as? UILabel)?.text = PayType.aliPay.payName
		(wechatView.viewWithTag(101) as? UILabel)?.text = PayType.wechatPay.payName
		alipayView.tag = PayType.aliPay.rawValue
		wechatView.tag = PayType.wechatPay.rawValue
		paysView.forEach { view in
			view.viewWithTag(102)?.layer.cornerRadius = 12
			view.viewWithTag(102)?.layer.borderWidth = 1
			view.viewWithTag(102)?.layer.borderColor = UIColor(red:0.91, green:0.91, blue:0.91, alpha:1.00).cgColor
			view.addGestureRecognizer(UITapGestureRecognizer(target: self,
															 action: #selector(MyntChargeViewController.didClickPayView(gestureRecognizer:))))
		}

		payType = .aliPay

		guard let mynt = sn?.mynt else { return }

		mynt.loadAvatar(block: { [weak self] image in
			self?.avatarImageView.image = image
		)}

		nameLabel.text = mynt.name

		updateExpiryTime()

		loadPriceList()
	}

	override func leftBatButtonClickHandler() {
		dismissNavigationController(animated: true)
	}

	//订单详情界面
	override func rightBarButtonLClickedHandler() {
		OrderListViewController.show(parentViewController: self, sn: sn)
	}

	override func updateProperty(mynt: Mynt, name: String, oldValue: Any?, newValue: Any?) {
		switch name {
		case "expiryTime", "usageValues", "name", "usage":
			updateExpiryTime()
		default:
			break
		}
	}

	func scrollViewDidScroll(_ scrollView: UIScrollView) {
		CATransaction.setDisableActions(true)
		infoBackgroundLayer.frame = CGRect(x: 0,
										   y: scrollView.contentOffset.y,
										   width: self.view.frame.width,
										   height: infoView.frame.height + scrollView.contentOffset.y * -1)
		CATransaction.setDisableActions(false)
	}

	func updateExpiryTime() {
		guard let mynt = sn?.mynt else { return }
		remainderNumLabel.text = "\(mynt.expiryDay)"
		remainderTimeLabel.text = mynt.expiryTimeString + NSLocalizedString("到期", comment: "")
	}

	fileprivate func loadPriceList() {
		SCPay.pricePackage(success: { [weak self] result in
			self?.package = result
		}) { _, message in
			Toast.show(message: message)
		}
		sn?.mynt?.simcardStatus()
	}

	func didClickPackageView(gestureRecognizer: UITapGestureRecognizer) {
		let view = gestureRecognizer.view
		for package in packages where view?.tag == package.month {
			selectedPackage = package
		}
	}

	func didClickPayView(gestureRecognizer: UITapGestureRecognizer) {
		guard let view = gestureRecognizer.view else { return }
		if let payType = PayType(rawValue: view.tag) {
			self.payType = payType
		}
	}

	@IBAction func didClickchargeButton(button: UIButton) {
		guard let selectedPackage = selectedPackage else { return }
		if payType == .aliPay {
			sn?.mynt?.aliPay(month: selectedPackage.month, success: { [weak self] params in
				PayReviewViewController.show(parentViewController: self, payParams: params)
			}) { message in
				Toast.show(message: message)
			} 
		} else if payType == .wechatPay {
			sn?.mynt?.wechatPay(month: selectedPackage.month, success: { [weak self] params in
				PayReviewViewController.show(parentViewController: self, payParams: params)
			}) { message in
				Toast.show(message: message)
			}
		}
	}
}


