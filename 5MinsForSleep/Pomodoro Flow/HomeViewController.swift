//
//  HomeViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/27.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import UIKit

class HomeViewController: UIViewController {

    @IBOutlet weak var runButton: UIButton!
    @IBOutlet weak var PushupButton: UIButton!


    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func clickPushupButton(_ sender: Any) {
        self.performSegue(withIdentifier: "PushupButton", sender: self)
    }


    @IBAction func clickRunButton(_ sender: Any) {
        self.performSegue(withIdentifier: "runButton", sender: self)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
