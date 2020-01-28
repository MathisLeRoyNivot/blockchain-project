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

    parsePages(page) {
        this.sender = page.sender;
        this.receiver = page.receiver;
        this.data = page.data;
        this.timestamp = page.timestamp;
    }
    /* Stringfying and Parser functions */
}

module.exports = Pages;