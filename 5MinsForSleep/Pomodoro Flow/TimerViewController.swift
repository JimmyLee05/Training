//
//  TimerViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit

class TimerViewController: UIViewController {

    @IBOutlet weak var startButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    @IBOutlet weak var pauseButton: UIButton!
    @IBOutlet weak var buttonContainer: UIView!
    @IBOutlet weak var collectionView: UICollectionView!

    @IBOutlet weak var timerLabel: UILabel! {
        didSet {
            // 在iOS 8和之前的系统中，数字默认等宽
            if #available(iOS 9.0, *) {
                timerLabel.font = UIFont.monospacedDigitSystemFont(ofSize: 124.0,
                                                                   weight: UIFontWeightUltraLight)
            }
        }
    }

    // 在这里引用三个类的单例
    fileprivate let scheduler: Scheduler
    fileprivate let pomodoro  = Pomodoro.sharedInstance
    fileprivate let bgMusic   = BgMusicViewController.sharedBgMusic

    // 时间
    fileprivate var timer: Timer?
    fileprivate var currentTime: Double!
    fileprivate var running = false

    // Configuration
    fileprivate let animationDuration = 0.3
    fileprivate let settings = SettingsManager.sharedManager

    fileprivate struct CollectionViewIdentifiers {
        static let emptyCell = "EmptyCell"
        static let filledCell = "FilledCell"
    }

    // Pomodoros view
    fileprivate var pomodorosCompleted: Int? = 0
    fileprivate var targetPomodoros: Int? = 0

    // MARK: - Initialization
    required init?(coder aDecoder: NSCoder) {
        targetPomodoros = settings.targetPomodoros
        pomodorosCompleted = pomodoro.pomodorosCompleted
        scheduler = Scheduler()

        super.init(coder: aDecoder)
    }

    deinit {
        NotificationCenter.default.removeObserver(self)
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        NotificationCenter.default
            .addObserver(self,
                         selector: #selector(willEnterForeground),
                         name: NSNotification.Name.UIApplicationWillEnterForeground, object: nil)

        bgMusic.playBgMusic()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)

        willEnterForeground()
    }

    // 进入后台前的设置
    func willEnterForeground() {
        print("willEnterForeground called from controller")

        setCurrentTime()
        updateTimerLabel()

        if scheduler.pausedTime != nil {
            //Button从下往上的一个动画
            animateStarted()
            animatePaused()
        }
        reloadData()
    }

    func secondPassed() {
        if currentTime > 0 {
            currentTime = currentTime - 1.0
            updateTimerLabel()
            return
        }
        print("State: \(pomodoro.state), done: \(pomodoro.pomodorosCompleted)")

        if pomodoro.state == .default {
            pomodoro.completePomodoro()
            reloadData()
        } else {
            pomodoro.completeBreak()
        }

        stopTimer()
        print("State: \(pomodoro.state), done: \(pomodoro.pomodorosCompleted)")
    }

    // MARK: - Actions
    @IBAction func togglePaused(_ sender: EmptyRoundedButton) {
        scheduler.paused ? timerUnpause() : timerPause()
    }

    @IBAction func start(_ sender: RoundedButton) {
        startTimer()
    }

    @IBAction func stop(_ sender: RoundedButton) {
        stopTimer()
    }
}

// TimerViewController里的一些函数放在拓展里，主控制器可以直接调用
extension TimerViewController {

    func startTimer() {
        scheduler.timeStart()
        running = true
        animateStarted()
        fireTimer()
        bgMusic.startBGMusic()
    }

    func stopTimer() {
        scheduler.timeStop()
        running = false
        animateStopped()
        timer?.invalidate()
        resetCurrentTime()
        updateTimerLabel()
        bgMusic.stopBGMusic()
    }

    func timerPause() {
        guard running else { return }

        scheduler.timePause(currentTime)
        running = false
        timer?.invalidate()
        animatePaused()
        bgMusic.stopBGMusic()
    }

    func timerUnpause() {
        scheduler.timeUnpause()
        running = true
        fireTimer()
        animateUnpaused()
        bgMusic.startBGMusic()
    }

    func presentAlertFromNotification(_ notification: UILocalNotification) {
        let alertController = UIAlertController(title: notification.alertTitle,
                                                message: notification.alertBody,
                                                preferredStyle: .alert)

        let okAction = UIAlertAction(title: "OK", style: .default) { action in print("OK") }
        alertController.addAction(okAction)

        present(alertController, animated: true, completion: nil)
    }

    // MARK: - Helpers
    fileprivate func reloadData() {
        targetPomodoros = settings.targetPomodoros
        pomodorosCompleted = pomodoro.pomodorosCompleted
        collectionView.reloadData()
    }

    fileprivate func updateTimerLabel() {
        let time = Int(currentTime)
        timerLabel.text = String(format: "%02d:%02d", time / 60, time % 60)
    }

    fileprivate func setCurrentTime() {
        if let pausedTime = scheduler.pausedTime {
            currentTime = pausedTime
            return
        }
        if let fireDate = scheduler.fireDate {
            let newTime = fireDate.timeIntervalSinceNow
            currentTime = (newTime > 0 ? newTime : 0)
            return
        }
        resetCurrentTime()
    }

    fileprivate func resetCurrentTime() {
        switch pomodoro.state {
        case .default: currentTime = Double(settings.pomodoroLength)
        case .shortBreak: currentTime = Double(settings.shortBreakLength)
        case .longBreak: currentTime = Double(settings.longBreakLength)
        }
        resetTimerLabelColor()
    }

    fileprivate func resetTimerLabelColor() {
        switch pomodoro.state {
        case .default: timerLabel.textColor = UIColor.accentColor
        case .shortBreak, .longBreak: timerLabel.textColor = UIColor.breakColor
        }
    }

    fileprivate func fireTimer() {
        timer = Timer.scheduledTimer(timeInterval: 1,
                                     target: self, selector: #selector(secondPassed), userInfo: nil, repeats: true)
    }

    fileprivate func refreshPomodoros() {
        targetPomodoros = settings.targetPomodoros
        collectionView.reloadData()
    }

    fileprivate func animateStarted() {
        let deltaY: CGFloat = 54
        buttonContainer.frame.origin.y += deltaY
        buttonContainer.isHidden = false

        UIView.animate(withDuration: animationDuration, animations: {
            self.startButton.alpha = 0.0
            self.buttonContainer.alpha = 1.0
            self.buttonContainer.frame.origin.y += -deltaY
        })
    }

    fileprivate func animateStopped() {
        UIView.animate(withDuration: animationDuration, animations: {
            self.startButton.alpha = 1.0
            self.buttonContainer.alpha = 0.0
        })

        pauseButton.setTitle("Pause", for: UIControlState())
    }

    fileprivate func animatePaused() {
        pauseButton.setTitle("Resume", for: UIControlState())
    }

    fileprivate func animateUnpaused() {
        pauseButton.setTitle("Pause", for: UIControlState())
    }
}

extension TimerViewController: UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {

    // MARK: UICollectionViewDataSource
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return numberOfSections
    }

    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int {
        return numberOfRows(inSection: section)
    }

    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {

        let index = rowsPerSection * indexPath.section + indexPath.row
        let identifier = (index < pomodorosCompleted!) ?
            CollectionViewIdentifiers.filledCell : CollectionViewIdentifiers.emptyCell

        return collectionView.dequeueReusableCell(withReuseIdentifier: identifier,
                                                for: indexPath)
    }

    // MARK: UICollectionViewDelegate
    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        insetForSectionAt section: Int) -> UIEdgeInsets {
        let bottomInset: CGFloat = 12
        return UIEdgeInsetsMake(0, 0, bottomInset, 0)
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 10.0
    }

    // MARK: Helpers
    fileprivate var rowsPerSection: Int {
        let cellWidth: CGFloat = 30.0
        let margin: CGFloat = 10.0
        return Int(collectionView.frame.width / (cellWidth + margin))
    }

    fileprivate func numberOfRows(inSection section: Int) -> Int {
        if section == lastSectionIndex {
            return numberOfRowsInLastSection
        } else {
            return rowsPerSection
        }
    }

    fileprivate var numberOfRowsInLastSection: Int {
        if targetPomodoros! % rowsPerSection == 0 {
            return rowsPerSection
        } else {
            return targetPomodoros! % rowsPerSection
        }
    }

    fileprivate var numberOfSections: Int {
        return Int(ceil(Double(targetPomodoros!) / Double(rowsPerSection)))
    }

    fileprivate var lastSectionIndex: Int {
        if numberOfSections == 0 {
            return 0
        }
        return numberOfSections - 1
    }
}
