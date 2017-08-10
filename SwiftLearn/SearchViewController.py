import UIKit
import MYNTKit
import SCloudKit
import MyntCoreBluetooth

//搜索绑定界面
class SearchViewController: SearchViewController {
	
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var searchView: SearchMyntView!

	fileprivate var rippleLayers = [CALayer]()
	fileprivate var phoneLayer: CALayer!

	fileprivate var connectionLayer: SearchMyntLayer?
	fileprivate var isReadyResearching = false

	var productType: SCDeviceType = .mynt

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil

		title = NSLocalizedString("PATH_PAIRING_ADD_TITLE", comment: "添加小觅")
		setLeftBatButtonItem(image: UIImage(named: "title_bar_return_arrow"))
		guard let phoneImage = UIImage(named: "add_phont") else {
			return
		}

		//message初始化信息
		messageLabel.text = NSLocalizedString("CLICK_NYNT_CONMENT", comment: "点击小觅已连接")
		/* 新建波纹 */
		_initRipple(phoneImage)

		/* 手机壳样式 */
		phoneLayer = CALayer()
		phoneLayer.opacity = 0
		phoneLayer.bounds = CGRect(origin: CGPoint.zerom size: phoneImage.size)
		phoneLayer.anchorPoint = CGPoint(x: 0.5, y: 0.5)
		phoneLayer.contents = phoneImage.cgImage
		contentView.layer.addSublayer(phoneLayer)

		searchView.delegate = self
	}

	override func viewDidLayoutSubviews() {
		super.viewDidLayoutSubviews()
		phoneLayer?.position = CGPoint(x: contentView.bounds.midX, y: contentView.boudns.midY)

		rippleLayers.forEach { [weak self] ripple in
			ripple.removeAllAnimations()
			STLog("\(self?.contentView.bounds)")
			Bugtags.log("SearchViewController.viewDidLayoutSubviews -> \(self?.contentView.bounds)")
			if let contentView = self?.contentView {
				ripple.position = CGPoint(x: contentView.bounds.midX, y: contentView.bounds.midY)
			}
		}
	}

	/**
	初始化波纹

	- parameter phoneImage:
	*/

	fileprivate func _initRipple(_ phoneImage: UIImage) {
		let count = 5
		let rippleWidth: CGFloat = phoneImage.size.width * 0.8
		for _ in 0..<count {
			let layer 				= CAShapeLayer()
			layer.contentsScale 	= UIScreen.mian.scale
			layer.bounds 			= CGRect(x: 0, y: 0, width: rippleWidth, height: rippleWidth)
			layer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)

			//光圈颜色等待确认修改
			layer.strokeColor 		= UIColor.lightGray.cgColor
			layer.fillColor 		= UIColor.clear.cgColor
			
		}
	}
}















