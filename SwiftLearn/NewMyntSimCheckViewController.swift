//
//  NewMyntSimCheckViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/17.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MarkdownView

extension Mynt.CheckSimError {
    
    var name: String {
        switch self {
        case .mobileBluetoothError:
            return MTLocalizedString("SIM_CHECK_PHONE_TITLE", comment: "")
        }
    }
    
    var message: String {
        switch self {
        case .mobileBluetoothError:
            return "SIM_ERROR_1"
        }
    }
}

extension Mynt.CheckSimProgress {
    
    var name: String {
        switch self {
        case .mobileBluetooth:
            return MTLocalizedString("")
        }
    }
    
    fileprivate static var all: [Mynt.CheckSimProgress] = [.mobileBluetooth,
                                                           .myntConnectState,
                                                           .mobileNet,
                                                           .myntSimState,
                                                           .myntNetState]
}

class MyntSimCheckViewController: BaseViewController {
    
    enum State {
        
        case ready
        
        var statusText: String {
            switch self {
            case .ready: return MTLocalizedString("SIM_CHECK_STATE_READY", comment: "欢迎使用 ！")
            }
        }
        var checkButtonText: String {
            switch self {
            case .ready: return MTLocalizedString("SIM_CHECK_BUTTON_START", comment: "开始检测")
            }
        }
    }
    
    public class func show(parentViewController: UIViewController?, mynt: Mynt?) {
        
    }
    
    @IBOutlet
    
    @IBOutlet
    
    fileprivate lazy var errorMessageLabel: MarkdownView = {
        let mdView = MrakdownView()
        self.errorMessageView.addSubview(mdView)
        mdView.translatesAutoresizingMaskIntoConstraints = false
        mdView.fillInSuperView()
        return mdView
    }()
    
    fileprivate var startTime = 0
    fileprivate var progress: Mynt.CheckSimProgress = .none {
        
    }
    fileprivate var errorCode: Int? = 0
    fileprivate var error: Mynt.CheckSimError? {
        didSet {
            self.state = .failed
            
            if let name = error?.name {
                
            }
            if let error = error {
                
            }
        }
    }
    
    fileprivate lazy var scanLayer: CALayer = {
        let layer = CALayer()
        layer.bounds = self.animationView.bounds
        
    }()
    
    var state: State = .ready {
        didSet {
            self.statusLabel.text = state.statusText
            self.checkButton.setTitle(state.checkButtonText, for: .normal)
            switch state {
            case .ready:
                self.statusImageView.image = nil
            }
            self.scanLayer.isHidden = state != .progress
        }
    }
    
    fileprivate lazy var animationBorder: CALayer = {
        let layer = CALayer()
        layer.boderColor    = UIColor.white.cgColor
        layer.borderWidth   = 2
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.navigationController?.isNavigationBarHidden = true
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
    }
    
    @IBAction func didClickCloseButton(_ sender: Any) {
        
    }
    
    fileprivate func closeViewController() {
        
    }
    
    @IBAction func didClickCheckButton(_ sender: Any) {
        switch state {
        case .ready:
            self.state = .progress
        case .progress:
            break
        case .failed:
            self.state = .progress
        case .success:
            closeViewController()
        }
    }
    
    //轮询调用，检测时间
    @objc func checkNetwork() {
        
    }
    
    func startCheck() {
        
    }
}

extension MyntSimCheckViewController: UIAlertViewDelegate {
    
    func alertView() {
        
    }
}

extension MyntSimCheckViewController: UITableViewDelegate, UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int)  -> Int {
        
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
    }
}

