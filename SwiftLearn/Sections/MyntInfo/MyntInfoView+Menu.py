import Foundation

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
	
	case cancel			= "SECURE_AREA_DELETE_CANCEL"
	case avator			= "MODIFY_AVATARS_AND_NAMES"
	case firmware		= "UPDATE_FIRMWARE"
	case disconnect		= "DISCONNECT"
	case charge			= "MYNT_GPS_DEPOSIT"
	case shutdown		= "MYNT_GPS_TURN"
	case share 			= "MYNT_GPS_SHARE"
	case delete 		= "REMOVE_THIS_MYNT"
	case tools			= "调试工具箱"

	var localized : String { return NSLocalizedString(rawValue, comment: "")}

	static func key(localized: String) -> Menu? {
		return iterateEnum(Menu.self).filter({localized == $0.localized}).first
	}
}

//MARK: -actionSheet
extension MyntInfoViewController: UIActionSheetDelegate {
	
	override func rightBarButtonCLickedHandler() {
		let actionSheet = UIActionSheet(title: nil,
										delegate: self,
										cancelButtonTitle: Menu.cancel.localized,
										destructiveButtonTitle: nil)
		var menus = [Menu]()
		guard let mynt = sn?.mynt else { return }
		switch mynt.myntType {
		case .mynt:
			menus.append(.avator)
			if mynt.hasNewFirmware {
				menus.append(.firmware)
			}
			if mynt.bluetoothState == .connection {
				menus.append(.disconnect)
			}
		case .myntGPS:
			if mynt.canEdit {
				menus.append(.avatar)
			if mynt.isOwner {
				switch mynt.simStatus {
				case .normal, .overdue, .deactivated:
					menus.append(.charge)
				default:
					break
				}
				menus.append(.share)
				menus.append(.shutdown)
				if mynt.hasNewFirmware {
					menus.append(.firmware)
				}
			}
		case .none:
			break
		}
		if AppConfig.isDebugMode {
			menus.append(.tools)
		}

		menus.append(.delete)
		menus.forEach { actionSheet.addButton(withTitle: $0.localized) }
		actionSheet.destructiveButtonIndex = actionSheet.numberOfButtons - 1
		actionSheet.show(in: view)
	}

	func actionSheet(_ actionSheet: UIActionSheet, didDismissWithButtonIndex buttonIndex: Int) {
		guard let mynt = sn?.mynt else { return }
		guard let title = actionSheet.buttonTitle(at: buttonIndex), let menu = Menu.key(localized: title) else { return }
		switch menu {
		case .avator:
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
		case .tools:
			break
		case .cancel: break
		}
	}
}

