import UIKit
import MYNTKit

fileprivate extension SCDeviceType {
	
	var image: UIImage? {
		switch self {
		case .none:
			return nil
		case .mynt:
			return UIImage(named: "app_product_add_mynt")
		case .myntGPS:
			return UIImage(named: "app_product_add_myntgps")
		}
	}
}

//选择产品
class SelectProductViewController: SearchBaseViewController {
	
	@IBOutlet weak var chooseLabel: UILabel!
	@IBOutlet weak var tableView: UILableView!

	let productTypes: [SCDeviceType] = [.mynt, .myntGPS]

	override func viewDidLoad() {

		super.viewDidLoad()
		setLeftBarButtonItem(image: UIImage(named: "title_bar_return_arrow"))
		title = NSLocalizedString("PAIR_CONNECTING_TITLE", comment: "添加小觅")

		tableView.register(with: SelectProductTableViewCell.self)
		tableView.estimatedRowHeight 	= 140
		tableView.rowHeight 			= UITableViewAutomaticDimension
		tableView.delegate 				= self
		tableView.dataSource 			= self

		chooseLabel.text = NSLocalizedString("PRODUCT_CHOOSE", comment: "提示语")
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}
}

extension SelectProductViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return productTypes.count
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: SelecrProductTableViewCell.self, for: indexPath)

		let item = productTypes[indexPath.row]
		cell?.productImageView.image 		= item.image
		cell?.productImageView.text 		= MYNT
		cell?.productTypeNameLabel.text 	= item.typeName
		cell?.setShowdowStyle(ShadowStyle.lButtonShadow)
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		let item = productTypes[indexPath.row]
		switch item {
		case .none:
			break
		case .mynt:
			let viewController = SearchTipsViewController()
			navigationController?.pushViewController(viewController, animated: true)
		case .myntGPS:
			let viewController = SearchGPSTipsViewController()
			navigationController?.pushViewController(viewController, animated: true)
		}
	}
}


