import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { AppService } from '../app.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-chat',
  templateUrl: './chat-new.component.html',
  styleUrls: ['./chat-new.component.css'],
})
export class ChatNewComponent implements OnInit {
  title = 'Chatbot';
  message = '';
  menuModal: any;
  selectedTopicsList: string[] = ['all'];

  @ViewChild('scrollMe') private myScrollContainer!: ElementRef;
  selectedTopics: { [key: string]: boolean } = {
    All: true,
    Health: false,
    Environment: false,
    Technology: false,
    Economy: false,
    Entertainment: false,
    Sports: false,
    Politics: false,
    Education: false,
    Travel: false,
    Food: false,
  };

  constructor(public appService: AppService, private modalService: NgbModal) {}

  ngOnInit() {}

  sendMessage() {
    if (this.message !== '') {
      const data = { user_input: this.message, topic: this.selectedTopicsList };
      this.appService.messageArray.push({
        name: 'user',
        message: this.message,
      });
      this.appService.query(data).subscribe((response: any) => {
        this.appService.messageArray.push({
          name: 'bot',
          message: response['final_output'],
        });
      });
      this.message = '';
    }
  }

  openMenuModal(content: any) {
    this.menuModal = this.modalService.open(content, { size: 'sm' });
  }
  closeMenu() {
    this.menuModal.close();
  }
  menuItem(item: string) {
    this.appService.messageArray.length = 0;
    this.menuModal.close();
  }

  updateSelectedTopics(topic: string) {
    if (topic === 'All') {
      this.selectedTopics = {
        All: true,
        Health: false,
        Environment: false,
        Technology: false,
        Economy: false,
        Entertainment: false,
        Sports: false,
        Politics: false,
        Education: false,
        Travel: false,
        Food: false,
      };
      this.selectedTopicsList = ['all'];
    } else {
      this.selectedTopics['All'] = false;
      this.selectedTopics[topic] = !this.selectedTopics[topic];
      // if (this.selectedTopics[topic]) {
      //   this.selectedTopicsList.push(topic);
      // } else {
      //   // this.selectedTopicsList = this.selectedTopicsList.filter(item => item !== topic);
      //   this.selectedTopicsList = Object.keys(this.selectedTopics).filter(
      //     (key) => this.selectedTopics[key]
      //   );
      // }
      this.selectedTopicsList = Object.keys(this.selectedTopics)
        .filter((key) => this.selectedTopics[key])
        .map((key) => key.toLowerCase());
      if (this.selectedTopicsList.length === 0) {
        this.selectedTopicsList = ['all'];
        this.selectedTopics['All'] = true;
      }
    }

    // {
    //   this.selectedTopics['All'] = false;

    //   this.selectedTopics[topic] = !this.selectedTopics[topic];

    //   this.selectedTopicsList = Object.keys(this.selectedTopics).filter(
    //     (key) => this.selectedTopics[key]
    //   );
    // }
  }
}
