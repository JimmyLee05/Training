import Foundation
import SlightechKit
import MYNTKit

extension Mynt {
	
	func updateStatusLabel(addressLabel: UILabel? = nil, simStatusLabel: UILabel? = nil) {
		if isInvalidated { return }
		//错误颜色
		let errorColor = UIColor(red:0.97, green:0.23, blue:0.20, alpha:1.00)
		//连接状态
		if bluetoothState == .connecting || bluetoothState == .connected {
			addressLabel?.text = distanceText
		} else {
			if coordinate.isNull {
				addressLabel?.text = distanceText
			} else {
				coordinate.offsetLocation.reverseGeocodeLocation(false) { [weak self] address in
					if self?.isInvalidated == true { return }
					let isShowDistance = self?.bluetoothState == .connecting || self?.bluetoothState == .connected || address == nil
					addressLabel?.text = isShowDistance ? self?.distanceText : address
					addressLabel?.textColor = self?.connectType == .bluetoothError ? errorColor : UIColor.white
				}
			}
		}
		addressLabel?.textColor = connectType == .bluetoothError ? errorColor : UIColor.white
		if myntType == .mynt {
			simStatusLabel?.text = disconnectTime
			simStatusLabel?.textColor = UIColor(red:0.64, green:0.65, blue:0.67, alpha:1.00)
			return
		}
		//SIM卡状态
		switch simStatus {
		case .normal:
			//显示断线时间
			if workStatus == .lowpower1 {
				//低电量
				simStatusLabel?.textColor = UIColor(red:0.29, green:0.79, blue:0.35, alpha:1.00)
				simStatusLabel?.text = NSLocalizedString("LOW_BATTERY_MODE", comment: "低电量模式")
				return
			}
			simStatusLabel?.text = disconnectTime
			simStatusLabel?.textColor = UIColor(red:0.64, green:0.65, blue:0.67, alpha:1.00)
		default:
			//显示卡状态
			simStatusLabel?.text = simStatus.simStatusText
			simStatusLabel?.textColor = errorColor
		}

	}
}

