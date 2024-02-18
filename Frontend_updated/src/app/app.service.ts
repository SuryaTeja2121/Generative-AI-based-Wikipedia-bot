import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root',
})
export class AppService {
  messageArray: any[] = []

  constructor(private httpClient: HttpClient) {}

  query(data: any) {
    let url = 'http://localhost:9999/chat'
    return this.httpClient.post(url, data)
  }
  stats() {
    let url = 'http://localhost:9999/get_topics'
    return this.httpClient.get(url)
  }
  sentiment_history() {
    let url = 'http://localhost:9999/sentiment_history'
    return this.httpClient.get(url)
  }
}
