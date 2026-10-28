interface SubscriberPolicy { readonly maxQueueBytes:number }
export const policy: SubscriberPolicy={maxQueueBytes:'64KiB'};
