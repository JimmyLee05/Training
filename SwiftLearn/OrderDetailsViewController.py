import UIKit
import SCloudKit

class OrderDetailsViewController: BaseViewController {
		
	public class func show(parentViewController: UIViewController?, order: SCPay.SCOrder?) {
		let viewController 			= OrderDetailsViewController()
		viewController.order 		= order
		parentViewController?.removeBackBarButtonTitle()
		parentViewController?.push(viewController: viewController)
	}

	override var isShowBackgroundLayer: Bool { return false}

	var order: SCPay.SCorder?

	@IBOutlet weak var moneyLabel: UILabel!

	@IBOutlet weak var payStateLabel: UILabel!

	@IBOutlet weak var numberTitle: UILabel!
	@IBOutlet weak var numberTitle: UILabel!

	@IBOutlet weak var dateTitle: UILabel!
	@IBOutlet weak var dateValue: UILabel!

	@IBOutlet weak var snTitle: UILabel!
	@IBOutlet weak var snValue: UILabel!

	@IBOutlet weak var payTypeTitle: UILabel!
	@IBOutlet weak var payTypeValue: UILabel!

	override func viewDidLoad() {
		super.viewDidLoad()
		initUI()
	}

	func initUI () {
		title = NSLocalizedString("支付详情", comment: "")

		guard let order = self.order else { return }
		moneyLabel.text = String(format: "%.2f", order.money)

		payStateLabel.text 			= order.orderStatus.statusName
		payStateLabel.textColor 	= order.orderStatus.textColor

		numberTitle.text = NSLocalizedString("订单号", comment: "")
		numberValue.text = order.orderNo
		numberValue.openCopyable()

		dateTitle.text = NSLocalizedString("支付日期", comment: "")
		dateValue.text = order.dateString

		snTitle.text = NSLocalizedString("设备识别号", comment: "")
		snValue.text = order.sn
		snValue.openCopyable()

		payTypeTitle.text = NSLocalizedString("支付方式", comment: "")
		payTypeValue.text = order.orderType.payTypeName
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

}


























