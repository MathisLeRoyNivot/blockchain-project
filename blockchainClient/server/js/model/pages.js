class Pages {
    constructor(sender, receiver, data) {
        this.sender = sender;
        this.receiver = receiver;
        this.data = data;
        this.timestamp = Date.now();
    }
    getDetails() {
        const {
            sender,
            receiver,
            data,
            timestamp
        } = this;
        return {
            sender,
            receiver,
            data,
            timestamp,
        };
    }

    parsePages(pages) {
        this.sender = pages.sender;
        this.receiver = pages.receiver;
        this.data = pages.data;
        this.timestamp = pages.timestamp;
    }
    /* Stringfying and Parser functions */
}

module.exports = Pages;