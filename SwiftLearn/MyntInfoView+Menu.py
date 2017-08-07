import Foundation

//遍历枚举
func iterateEnum<T: Hashable>(_: T.Type) -> AnyIterator<T> {
	var i = 0
	return AnyIterator {
		let next = withUnsafePointer(to: &i) {
			$0.withMemoryRebound(to: T.self, capacity: 1) { $0.pointee }
		}
		if next.hashValue != i { return nil }
		i += 1
		return next
	}
}

fileprivate enum Menu: String {
	
	case cancel 		= "SECURE_AREA_DELETE_CANCEL"
	case avatar 		= "MODIFY_AVATARS_AND_NAMES"
	case firmware 		= "UPDATE_FIRMWARE"
	case disconnect 	= "DISCONNECT"
	case charge 		= "MYNT_GPS_DEPOSIT"
	case shutdown 		= "MYNT_GPS_TURN"
	case share 			= "MYNT_GPS_SHARE"
	case delete 		= "REMOVE_THIS_MYNT"
	case simtest 		= "SIM卡检测"
	case iccid 			= "readIccid"


	var localized: String { return NSLocalizedString(rawValue, comment: "") }

	static func key(localized: String) -> Menu? {
		return iterateEnum(Menu.self).first(where: { localized == $0.localized })
	}
}

//MARK: - actionSheet
extension MyntInfoViewController: UIActionSheetDelegate {
	
	override func rightBarButtonClickedHandler() {
		let actionSheet = UIActionSheet(title: nil,
										delegate: self,
										cancelnButtonTitle: Menu.cancel.localized,
										destructiveButtonTitle: nil)
		var menus = [Menu]()
		guard let mynt = sn?.mynt else { return }
		switch mynt.myntType {
		case .mynt:
			menus.append(.avatar)
			if mynt.hasNewFirware {
				menus.append(.formware)
			}
			if mynt.bluetoothState == .connected {
				menus.append(.disconnect)
			}
		case .myntGPS:
			if mynt.canEdit {
				menus.append(.avatar)
			}
			if mynt.isOwner {
				switch mynt.simStatus {
				case .normal, .overdue, .deactivated:
					menus.append(.charge)
				default: 
					break
				}
				menus.append(.share)
				menus.append(.shutdown)
				memus.append(.simtest)
				menus.append(.iccid)

				if mynt.hasNewFirmware {
					menus.append(.firmware)
				}
			}
		case .none:
			break
		}

		menus.append(.delete)
		menus.forEach { actionSheet.addButton(withTitle: $0.localized) }
		actionSheet.destructiveButtonIndex = actionSheet.numberofButtons - 1
		actionSheet.show(in: view)
	}

	func actionSheet(_ actionSheet: UIActionSheet, didDismissWithButtonIndex buttonIndex: Int) {
		guard let mynt = sn?.mynt else { return }
		guard let title = actionSheet.buttonTitle(at: buttonIndex), let menu = Menu.key(localized: title) else { return }
		switch menu {
		case .avatar:
			didClickInfoView(isClickMenu: true)
		case .charge:
			MyntChargeViewController.show(parentViewController: self, sn: sn)
		case .share:
			ShareListViewController.show(parentViewController: self, sn: sn)
		case .shutdown:
			mynt.shutdown()
		case .firmware:
			UpdateFirmwareViewController.show(parentViewController: self, sn: sn)
			case .disconnect:
			mynt.disconnect()
		case .delete:
			didClickRemoveButton()
		case .simtest:
			MyntSimCheckViewController.show(parentViewController: self, sn: sn)
		case .iccid:
			mynt.readICCID(isIgnoreTime: true)
		case .cancel: 
			break
		}
	}
}


