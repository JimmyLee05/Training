import Foundation

extension MyntInfoViewController: MYNTKitDelegate {
	
	func initMyntListener() {
		MYNTKit.shared.addMyntKitDelegate(key: selfkey, delegate: self)
	}

	func initData() {
		guard let mynt = sn?.mynt else { return }
		if mynt.myntType == .myntGPS {
			mynt.downloadActivityInfo()
			mynt.simcardstatus()
		}
	}

	func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		if sn != mynt.sn { return }
		contentView?.uiState = mynt.uiState
		contentView?.tipsView.uiState = mynt.uiState
		if mynt.bluetoothState == .connected {
			//需要获取当前经纬度
			LocationManager.shared.requestLocation(handler: { [weak self] location, status in
				if let coordinate = location?.coordinate {
					self?.updateCoordinate(coordinate: coordinate)
				}
			})
		} 
	}

	//更新属性
	func _updateProperty(mynt:Mynt, name: String, oldValue: Any?, newValue: Any?) {
		if mynt.sn != sn { return }
		switch name {
		case "lostState":
			contentView?.uiState = mynt.uiState
			updateMapUI()
		case "latitude", "longitude":
			updateCoordinate(coordinate: mynt.coordinate)
		case "stepGoal", "calGoal", "step", "cal", "activityAlarmStep":
			contentView?.activityView.updateUIData()
		case "name", "battery", "simStatus", "workStatus", "isOwner", "pic", "latitude", "longitude", "canEdit":
			//更新基础信息
			contentView?.infoView.updateUIData()
			contentView?.updateNavigationBar()
			if name == "pic" {
				updateAvatarMapShot()
			}
		case "firmware", "hardware", "software":
			contentView?.removeView.updateUIData()
		case "uasge":
			updateAvatarMapShot()
			contentView?.infoView.updateUIData()
			contentView?.lossView.updateUIData()
		case "usageValues":
			contentView?.lossView.updateUIData()
		case "control":
			contentView?.controlExpandView.updateUIData()
		case "controlValues":
			contentView?.controlExpandView.updateUIData()
		case "isShowWillOverdueDialog":
			showSimWillDeactivatedDialog()
		case "isShowDeactivatedDialog":
			showSimDeactivatedDialog()
		default:
			break
		}
	}
}








