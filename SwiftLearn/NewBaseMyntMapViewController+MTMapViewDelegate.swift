//
//  NewBaseMyntMapViewController+MTMapViewDelegate.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/1.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation

extension BaseMyntMapViewController {
    
    // 释放地图
    func releaseMapView() {
        mapView.applyMapViewMemoryFix()
    }
    
    // 更新头像
    func updateAvatar(color: UIColor? = UIColor(red:0.50, green:0.67, blue:0.99, alpha:1.00), block: (() -> Void)? = nil) {
        mynt?.annotationImage(showOffline: false, color: color) { [weak self] image in
            self?.myntAnnotationImage = image
            block?()
        }
    }
    
    // 更新半径圈
    func updateRadiusCircle(coordinate: CLLocationCoordinate2D, stationCoordinate: CLLocationCoordinate2D? = nil) {
        if radiusCircle != nil {
            mapView.remove(radiusCircle!)
        }
        if stationCoordinate == nil { return }
        let radius = coordinate.distance(from: stationCoordinate!)
        if !stationCoordinate!.isNull && radius < maxRadius {
            //半径圈
            radiusCircle = MKCircle(enter: coordinate, radius: radius)
            mapView.add(radiusCircle!)
        }
    }
    
    // 更新图钉
    func updateMyntAnnotation(coordinate: CLLocationCoordinate2D,
                              item: MyntMapTimeLineView.TimeLine,
                              isNeedOffset: Bool = false) {
        let offSetCoordinate = isNeedOffset ? coordinate.offsetLocation : coordinate
        if myntAnnotation == nil {
                myntAnnotation = MTMyntAnnotation(sn: mynt?.sn, coordinate: offSetCoordinate)
                mapView.addAnnotation(myntAnnotation!)
        }
        dateLabel.text = item.itemString
        myntAnnotation?.coordinate = offSetCoordinate
        
        if !isShowPath {
            if isResetTimeline {
                mapView.show([offSetCoordinate], animated: true)
            } else {
                mapView.setCenter(offSetCoordinate, animated: true)
            }
        }
        
        // 反地理
        coordinate.reverseGeoCodeLocation { [weak self] address, _ in
            self?.locationLabel.text = address
            
            let formatter = DateFormatter()
            formatter.dateFormat = "yyyy-MM-dd HH:mm"
            self?.dateLabel.text = formater.string(from: Date(timeIntervalSince1970: TimeInterval(time)))
            self?.dateLabel.text = MTLocalizedString("DISCONNECT_TIME_NOW", comment: "now")
        }
    }
    
    func removeRadiusCircle() {
        if let radiusCircle = radiusCircle {
            mapView.remove(radiusCircle)
        }
    }
    
    func removeMyntAnnotation() {
        if let myntAnnotation = myntAnnotation {
            mapView.removeAnnotation(myntAnnotation)
        }
    }
}


// MARK: - MTMapViewDelegate
extension BaseMyntMapViewController: MTMapViewDelegate {
    
    public func mapViewDidClickBackButton(_ mapView: MTMapView) {
        mapView.move(mapView.userLocation.coordinate)
    }
    
    public func mapViewDidRenderDone(_ mapView: MTMapView) {
        loadSourceLocations()
    }
    
    public func mapView(_ mapView: MKMapView, didUpdate userLocation: MKUserLocation) {
        // 更新用户位置
        if let userLocation = userLocation.location {
            self.userCoordinate = userLocation.coordinate
            self.userCoordinateTime = Date().timeIntervalSince1970
            self.userCoordinateRadius = Int()
            
            updateUserLocation()
        }
    }
    
    public func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
        if let circle = overlay as? MKCircle {
            let circleView          = MKCircleRenderer(circle: circle)
            circleView.loadStyle()
            return circleView
        }
        if let polyline = overlay as? MKPolyline {
            let polylineRenderer            = MKPolylineRenderer(polyline: polyline)
            polylineRenderer.strokeColor    = UIColor(red:0.40, green:0.58, blue:0.94, alpha:1.00)
            polylineRenderer.lineWidth      = 6
            return polylineRenderer
        }
        return MKOverlayRenderer()
    }
    
    // 更新大头针新点
    public func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        if annotation is MKUserLocation {
            (annotation as? MKUserLocation)?.title = ""
            return nil
        }
        if let annotation = annotation as? MTAnnotation {
            switch annotation.tag {
            case pathStartAnnotationTag:
                var view = mapView.dequeueReusableAnnotationView(withIdentifier: "start")
                if view == nil {
                    view = MKAnnotationView(annotation: annotation, reuseIdentifier: "start")
                    view?.canShowCallout = false
                }
                view?.image = UIImage(named: "map_start")
                view?.layer.zPosition = 999
                
                view?.transform = CGAffineTransform(rotationAngle: pathStartAngle)
                return view
            case pathArrowAnnotationTag:
                var view = mapView.dequeueReusableAnnotationView(withIdentifier: "path_arrow")
                if view == nil {
                    view = MKAnnotationView(annotation: annotation, reuseIdentifier: "path_arrow")
                    view?.canShowCallout = false
                }
                view?.image = UIImage(named: "map_arrow")
                view?.layer.zPosition = 998
                
                view?.transform = CGAffineTransform(rotationAngle: annotation.angle)
                return view
            default:
                break
            }
        }
        
        if annotation is MTMyntAnnotation && myntAnnotationImage != nil {
            var view = mapView.dequeueReusableAnnotationView(withIdentifier: "mynt")
            if view == nil {
                view = MKAnnotationView(annotation: annotation, reuseIdentifier: "mynt")
                view?.canShowCallout = false
                view?.centerOffset = CGPoint(x: 0, y: -myntAnnotationImage!.size.height / 2 + 10)
            }
            view?.image = myntAnnotationImage
            view?.layer.zPosition = 1000
            return view
        }
        
        return MKAnnotationView()
    }
}
