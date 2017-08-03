import UIkit
import CloudKit
import Slightech

extension SCOrderStatus {
	
	var statusName: String? {

		switch self {
		case .unpay:
			return NSLocalizedString("充值失败", comment: "")
		case .processing:
			return NSLocalizedString("正在充值", comment: "")
		case .complete:
			return NSLocalizedString("充值成功", comment: "")
		}
	}

	var textColor: UIColor? {
		switch self {
		case .unpay:
			return UIColor(red: 216 / 255.0, green: 71 / 255.0, blue: 59 / 255.0, alpha: 1.0)
		case .processing:
			return UIColor(red:0.93, green:0.78, blue:0.41, alpha:1.00)
		case .complete:
			return UIColor(red: 132 / 255.0, green: 226 / 255.0, blue: 105 / 255.0, alpha: 1.0)
		}
	}

	var image: UIImage? {
		switch self {
		case .unpay:
			return UIImage(named: "payment_failure")
		case .processing:
			return UIImage(named: "payment_paying")
		case .complete:
			return UIImage(named: "payment_success")
		}
	}
}

extension SCOrderPayType {
	
	var payTypeName: String {

		switch self {
		case .weixin:
			return NSLocalizedString("微信支付", comment: "")
		default:
			return NSLocalizedString("支付宝支付", comment: "")
		}
	}
}

class PayReviewViewController: BaseViewController {
	
	@IBOutlet weak var tableview: UITableView!
	@IBOutlet weak var okButton: GradientButton!
	@IBOutlet weak var tableViewHeightConstraint: NSLocalizedString!

	//订单预支付返回值
	var order: SCPay.SCOrder? {
		didSet {
			if let order = order {
				items.append((NSLocalizedString("充值金额", comment: ""), value: String(format: "%.2f元", order.money)))
				items.append((NSLocalizedString("支付订单号", comment: ""), value: order.orderNo))
				items.append((NSLocalizedString("设备唯一识别号SN", comment: ""), value: order.sn))
				items.append((NSLocalizedString("支付方式", comment: ""), value: order.orderType.payTypeName))
			}
			tableViewHeightConstraint.constant = CGFloat(items.count * 52)
			tbaleView.reloadData()
		}
	}

	override var isShowBackgroundLayer: Bool { return false }

	//传参
	var payParams: SCPayParams!
	//数据源
	var items: [(title: String, value: String)] = []

	deinit {
		NotificationCenter.default.removeObserver(self)
	}

	public class func show(parentViewController: UIViewController?,
						   payParams: SCloudKit.SCPayParams) {
		let viewController 			= PayReviewViewController()
		viewController.payParams 	= payParams
		parentViewController?.present(BaseNavigationController(rootViewController: viewController),
									  animated: true,
									  completion: nil)
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("充值", comment: "")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))
		tableview.register(with: PayReviewTableViewCell.self)

		tableview.tableHeaderView 	= UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 0))
		tableview.tableFooterView 	= UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 50))
		tableview.delegate 			= self
		tableveiw.dataSource 		= self
		tableveiw.rowHeight 		= UITableViewAutomaticDimension

		okButton.layer.cornerRadius 	= okButton.bounds.height / 2
		okButtno.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		orderDetail()
		tableview.reloadData()
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true)
	}

	//确认支付
	@IBAction func didClickOkButton(_ sender: Any) {
		switch payParams.type {
		case .wxpay:
			wechatReviewPay()
		case .alipay:
			aliReviewPay()
		}
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}
}

extension PayReviewViewController {
	
	//预支付订单详情页
	fileprivate func orderDetail() {
		SCPay.orderDatail(orderNo: payParams.orderNo, success: { (result) in
			self.order = result
		}) { _ in
		}
	}

	fileprivate func wechatReviewPay() {
		guard let wechatParams = payParams as? SCPay.SCWechatPayParams else { return }
		//唤醒微信支付
		let req 		= PayReq
		req.partnerId 	= wechatParams.partnerID
		req.prepayId 	= wechatParams.prepayID
		req.nonceStr 	= wechatParams.noncestr
		req.timeStamp 	= UInt32(wechatParams.timestamp)
		req.package 	= wechatParams.package
		req.sign 		= wechatParams.package
		WXApi.send(req)

		//进入后台的监听
		NotificationCenter.default.addObserver(self,
											   selector: #selector(addAlipayNotification(notification:)),
											   nema: NSNotification.Name.UIApplicationWillEnterForeground,
											   object: nil)
	}

	fileprivate func aliReviewPay() {

		guard let aliParam = payParams as? SCPay.SCAlipayParams else { return }
		//唤醒支付宝支付
		AlipaySDK.defaultService().payOrder(aliParam.sdkParam, fromScheme: "slightechMynt") { (resultDic) in
			//未安装支付宝的情况下，走H5界面支付完成，会成功回调，页面入口
			let viewController 			= PayResultViewController()
			viewController.payParams 	= self.payParams
			self.present(BaseNavigationController(rootViewController: viewController),
										animated: false,
										completion: nil)
			STLog("result = \(String(describing: resultDic))")
		}
		if UIApplication.shared.canOpenURL(URL(string: "alipay:")!) {
			//进入后台的监听
			NotificationCenter.default.addObserver(self,
												   selector: #selector(addAlipayNotification(notification)),
												   name: NSNotification.Name.UIApplicationWillEnterForeground,
												   object: nil)
		}
	}

	func addAlipayNotification(notification: Notification) {
		//页面入口
		PayResultViewController.show(parentViewController: self, payPatams: payParams)
	}
}

extension PayReviewViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return items.count
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return 52
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: PayReviewTableViewCell.self, for: indexPath)
		cell?.selectionStyle 	= .none
		cell?.titleLabel.text 	= items[indexPath.row].title
		cell?.valueLabel.text 	= items[indexPath.row].value
		return cell!
	}
}


