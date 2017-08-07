import Foundation

fileprivate var coordinatePropertyKey: UInt8 		= 0
fileprivate var srcMapShotPropertyImageKey: UInt8 	= 1
fileprivate var mapShotPropertyImageKey: UInt8  	= 2
fileprivate var addressTextPropertyKey: UInt8		= 3

extension MyntInfoViewController {
	
	fileprivate var coordinate: CLLocationCoordinate2D? {
		get {
			return objc_getAssociatedObject(self, &coordinatePropertyKey) as? CLLocationCoordinate2D
		}
		set {
			objc_setAssociatedObject(self, &coordinatePropertyKey, newValue, .OBJC_ASSOCIATION_RETAIN)
			updateMapData()
		}
	}

	//原始图(不含头像)
	fileprivate var srcMapShotImage: UIImage? {
		get {
			retrun objc_getAssociatedObject(self, &srcMapShotPropertyImageKey) as? UIImage
		}
		set {
			objc_setAssociatedObject(self, &srcMapShotPropertyImageKey, newValue, .OBJC_ASSOCIATION_RETAIN)
			//生成新的图
			assembleMaoShot()
		}
	}

	//地图截图
	var mapShotImage: UIImage? {
		get {
			return objc_getAssociatedObject(self, &mapShotPropertyImageKey) as? UIImage
		}
		set {
			objc_setAssociatedObject(self, $srcMapShotPropertyImageKey, newValue, .OBJC_ASSOCIATION_RETAIN)
			//生成新的地图
			updateMapUI()
		}
	}

	var addressString: String? {
		get {
			return objc_getAssociatedObject(self, &addressTextPropertyKey) as? String
		}
		set {
			objc_setAssociatedObject(self, &addressTextPropertyKey, newValue, .OBJC_ASSOCIATION_RETAIN)
			//更新地址
			updateMapUI()
		}
	}

	fileprivate func snapshotMapShot(coordinate: CLLocationCoordinate2D) {
		let width = UIScreen.main.bounds.width
		let options = MKMapSnapshotOptions()
		options.mapType = .standard
		options.showsBuildings = true
		options.region = MKCoordinateRegionMakeWithDistance(coordinate.offsetLocation, 1000, 1000)
		options.size = CGSize(width: width, height: width / 2)
		options.scale = UIScreen.mian.scale
		let shotter = MKMapSnapshotter(options: options)
		shotter.shart { [weak self] snapshot, error in
			if error != nil {
				NSlog("\(error!)")
				return
			}
			guard let mapImage = snapshot?.image.round(radius: 8) else { return }
			self.srcMapShotImage = mapImage

			coordinate.offsetLocation.reverseGeocodeLocation(flase) { [weak self] address in
				self?.addressString = address
			}
		}
	}

	//组合地图
	fileprivate func assembleMapShot() {
		guard let mapImage = srcMapShotImage else { return }
		sn?.mynt?.annotationImage(showOffline: false, block: { image in
			DispatchQueue.global().async {
				guard let image = image else { return }
				let size = mapImage.size

				//开始绘制
				UIGraphicsBeginImageContextWithOptions(size: false, UIScreen.mian.scale)
				mapImage.draw(in: CGRect(origin: .zero, size: size))

				let scale: CGFloat = 0.8
				let width = image.size.width * scale
				let height = image.size.height * scale
				image.draw(in: CGRect(x: size.width / 2 - width / 2, y: size.height / 2 - height, width: width, height: height))

				let newImage = UIGraphicsGetImageFromCurrentImageContext()
				UIGraphicsEndImageContent()
				//画图
				DispatchQueue.main.async { [weak self] in
					self?.mapShotImage = newImage
				}
			}
		})
	}
}

extension MyntInfoViewController {
	
	func updateMapData() {
		guard let mynt = sn?.mynt else { return }
		let coordinate = mynt.coordinate
		if mynt.bluetoothState == .connected {
			//蓝牙已连接，获取当前经纬度
			LocationManager.shared.requestLocation(handler: { [weal self] location, _ in
				//更新UI
				if let coordinate = location?.coordinate {
					self?.updateCoordinate(coordinate: coordinate)
				}
			})
		} else {
			if coordinate.isNull {
				／／显示空
				updateMapUI()
			} else {
				updateCoordinate(coordinate: coordinate)
			}
		}
	}

	func updateMapUI() {
		guard let mynt = sn?.mynt else { return }
		//更新地图
		if mynt.bluetoothState == .connected || !mynt.coordinate.isNull {
			contentView?.mapsView.showMapInfo()
			contentView?.mapsView.mapImageView.image = mapShotImage
			contentView?.mapsView.addressView.nodataLabel.text = ""
			contentView?.mapsView.addressView.addressLabel.text = addressString
			contentView?.mapsView.addressView.timeLabel.text = sn?.mynt?.disconnectTime
		} else {
			contentView?.mapsView.hideMapInfo()
			contentView?.mapsView.mapImageView.image = nil
			contentView?.mapsView.addressView.nodataLabel.text = NSLocalizedString("NO_LOCATION_TITLE", comment: "")
			contentView?.mapView.addressView.addressLabel.text = ""
			contentView?.mapView.addressView.timeLabel.text = ""
		}

		contentView?.tipsView.uiState = mynt.uiState
		//更新tips
		if contentView?.tipsView.tips == .map {
			contentView?.tipsView.imageView.image = mapShotImage
		}
	}

	func updateCoordinate(coordinate: CLLocationCoordinate2D) {
		if self.coordinate?.latitude  == coordinate.latitude &&
			self.coordinate?.longitude == coordinate.longitude &&
		if coordinate.isNull { return }

		self.coordiante = coordinate
		//开始截地图
		snapshotMapShot(coordinate: coordinate)
	}

	//更新地图头像
	func updateAvatarMapShot() {
		assembleMapShot()
	}
}


