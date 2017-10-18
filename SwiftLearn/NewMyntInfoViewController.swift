//
//  NewMyntInfoViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/18.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import LeanCloud

class MyntInfoViewController: MYNTKitBaseViewController {
    
    class func push() {
        DispatchQueue.main.async {
            
        }
    }
    
    override var isShowBackgroundLayer: Bool { return false }
    
    var contentView: MyntInfoView?
    
    fileprivate init(mynt: Mynt?) {
        
    }
    
    fileprivate override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
        
    }
    
    internal required init?(coder aDecoder: NSCoder) {
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        initNavigationBar()
        initView()
        
        initData()
        updaloadLeanCloud()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        setNavigationBarBackground()
    }
    
    override func update() {
        contentView?.infoView.updateStatusLabel()
        contentView?.mapsView.updateUIData()
    }
    
    func uploadLeanCloud() {
        if let mynt = mynt,
            let software = Int(mynt.software) {
            if software >= 29 && mynt.myntType == .mynt {
                LeanCloudManager.shared.uploadBatterMynt(sn: mynt.sn)
            }
        }
    }
}



