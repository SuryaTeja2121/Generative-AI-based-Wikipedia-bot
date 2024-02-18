import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core'
import { BrowserModule } from '@angular/platform-browser'
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module'
import { AppComponent } from './app.component'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { FormsModule } from '@angular/forms'
import { MatRadioModule } from '@angular/material/radio'
import { MatButtonModule } from '@angular/material/button'
import { HttpClientModule } from '@angular/common/http'
import { MatIconModule } from '@angular/material/icon'
import { AppService } from './app.service'
import { ChatNewComponent } from './chat-new/chat-new.component';

// import { TestComponent } from './test/test.component'
import { LiveAnalyticsComponent } from './live-analytics/live-analytics.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  declarations: [AppComponent, ChatNewComponent, LiveAnalyticsComponent],

  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    MatRadioModule,
    MatButtonModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatIconModule,
    NgbModule
  ],
  providers: [AppService],
  bootstrap: [AppComponent],
  schemas: [NO_ERRORS_SCHEMA]
})
export class AppModule {}
