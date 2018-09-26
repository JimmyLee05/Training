//
//  CameraViewController.swift
//  HanCam
//
//  Created by 李南君 on 2018/9/26.
//  Copyright © 2018 NanJun Li. All rights reserved.
//

import UIKit

class CameraViewController: UIViewController {

    lazy var photos: UIImagePickerController = {
        let photos = UIImagePickerController()
        photos.sourceType = .photoLibrary
        photos.delegate = self
        return photos
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func openCameraAction(_ sender: Any) {

//        let openCameraVC = CameraController()
//        present(openCameraVC, animated: true, completion: nil)
    }

    @IBAction func openPhotosAction(_ sender: Any) {

        //        let photosVc = PhotosController()
        //        present(photosVc, animated: true, completion: nil)
        //present(photos, animated: true, completion: nil)

    }

}


extension CameraViewController: UIImagePickerControllerDelegate,UINavigationControllerDelegate {

    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {

//        picker.dismiss(animated: true, completion: nil)
//        let photosVC = PhotosController()
//        let img = info[UIImagePickerControllerOriginalImage] as! UIImage
//        photosVC.chooseImage = img.imgScale(width: SCREENW)
//        present(photosVC, animated: true, completion: nil)
    }

}
