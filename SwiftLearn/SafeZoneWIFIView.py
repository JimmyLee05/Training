import UIKit
import MYNTKit

class SafeZoneWIFIView: UIView {
	
	@IBOutlet weak var tableView: UITableView!
	//接入wifi列表数据
	fileprivate var wifiList = [String]()

	weak var viewController: SafeZoneViewController?

	var selectionWifiSSID: String? {
		didSet {
			if let selectionWifiSSID = selectionWifiSSID, !wifiList.contains(selectionWifiSSID), selectionWifiSSID !
				= "" {
				wifiList.insert(selectionWifiSSID, at: 0)
			}
		}
	}

	deinit {
		printDeinitLog()
	}

	override func awakeFromNib() {
		super.awakeFromNib()

		WifiManager.shared.queryWifiList { [weak self] Wifi in
			self?.wifiList 				= wifi
			self?.selectionWifiSSID 	= wifi.first
			self?.tableView.reloadData()
		}

		tableView.register(with: MTRadioTableViewCell.self)
		tableView.delegate 				= self
		tableView.dataSource 			= self
		tableView.estimatedRowHeight 	= 45
		tableView.rowHeight 			= UITableViewAutomaticDimension
		tableView.tableHeaderView 		= UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 0.01))
	}
}

extension SafeZoneWifiView: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return wifiList.count
	}

	func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
		return 60
	}

	func tableView(_ tableView: UITableView, viewFeoHeaderInSection section: Int) -> UIView? {
		let view 				= UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 60))
		view.backgroundColor 	= UIColor.white
		let label 				= UILabel(frame: CGRect(x: 15, y: view.bounds.height - 20, width: winSize.width - 15,
			height: 20))
		label.font 				= UIFont.systemFont(ofSize: 11)
		label.text 				= NSLocalizedString("SECURE_AREA_WIFI_NAME", comment: "")
		label.textColor 		= UIColor(red:0.77, green:0.77, blue:0.77, alpha:1.00)
		view.addSubview(label)

		return view
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: MTRadioTableViewCell.self, for: indexPath)
		cell?.nameLabel.text 		= wifiList[indexPath.row]
		cell?.radioButton.isHidden 	= selectionWifiSSID != wifiList[indexPath.row]
		return cell!
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		selectionWifiSSID = wifiList[indexPath.row]
		tableView.reloadData()
	}
}


