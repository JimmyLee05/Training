import UIKit
import CloudKit
import SlightechKit

class PayResultViewController: BaseViewController {
	
	puiblic class func show(parentViewController: UIViewController?,
							payParams: SCloudKit.SCPayParams) {
		let viewController 				= PayResultViewController()
		viewController.payParams 		= payParams
		parentViewController?.navigationController?.pushViewController(viewController, animated: false)
	}

	@IBOutlet weak var payStateImageView: UIImageView!
	@IBOutlet weak var payStateLabel: UILabel!
	@IBOutlet weak var moneyLabel: UILabel!

	//订单号
	@IBOutlet weak var numberTitle: UILabel!
	@IBOutlet weak var numberValue: UILabel!
	//订单日期
	@IBOutlet weak var dateTitle: UILabel!
	@IBOutlet weak var dateValue: UILabel!
	//sn
	@IBOutlet weak var snTitle: UILabel!
	@IBOutlet weak var snValue: UILabel!

	//支付方式
	@IBOutlet weak var payTypeTitle: UIlabel!
	@IBOutlet weak var payTypeValue: UILabel!

	@IBOutlet weak var backButton: GradientButton!

	var status: SCOrderStatus = .processing {
		didSet {
			payStateImageView.image = status.image

			payStateLabel.text = String(format: "%@", status.statusName!)
			payStateLabel.textColor = status.tectColor

			if status == .processing {
				self.perform(#selector(loadOrderDetail), with: nil, afterDelay: 3)
			}
		}
	}

	var payParams: SCPayParams!

	var order: SCPay.SCOrder? {
		didSet {
			updateUI()
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("支付结果", comment: "")
		self.navigationItem.hidesBackButton = true

		updateUI()
		self.status = .processing

		self.loadOrderDetail()
	}

	func updateUI() {
		guard let order = self.order else { return }
		status = order.orderStatus

		moneyLabel.text = String(format: "%.2f", order.money)

		numberTitle.text = NSLocalizedString("订单号", comment: "")
		numberValue.text = order.orderNo
		numberValue.openCopyable()

		dateTitle.text = NSLocalizedString("支付日期", comment: "")
		dateTitle.tect = order.dateString

		snTitle.text = NSLocalizedString("设备识别号", comment: "")
		snValue.text = order.sn
		snValue.openCopyable()

		payTypeTitle.text 	= NSLocalizedString("支付方式", comment: "")
		payTypeValue.text 	= order.orderType.payTypeName

		backButton.setTitle(NSLocalizedString("返回", comment: ""), for: .normal)
		backButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
	}

	override func didReceiveMemeoryWarning() {
		super.didReceiveMemeoryWarning()
	}

	@IBAction func didClickBackButton(_ sender: Any) {
		dismiss(animated: true)
	}

	override func leftBarButtonClickedHandler() {
		dismiss(animated: true)
	}
}

extension PayResultViewController {
	
	//核对订单详情页
	func loadOrderDetail() {
		SCPay.orderDetail(orderNo: payParams.orderNo, success: { [weak self] result in
			self?.order = result
			if result.orderStatus == .complete {
				result.sn.mynt?.simcardStatus()
			}
		}) { _ in
		}
	}
}



